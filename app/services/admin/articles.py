from datetime import datetime

from tortoise.transactions import in_transaction, atomic

from app.cache.articles import ArticleCacheService
from app.core.enums import BlogErrorEnum
from app.core.exceptions import BlogException
from app.models import User, Article, Category, Tag
from app.schemas.admin.articles import ArticleCreateParam, ArticleUpdateParam, ArticlePageParam, ArticlePageItemResult, \
    ArticleUpdateStatusParam, ArticleDetailResult
from app.schemas.common import IdParam, ApiPageResult


class ArticleAdminService:

    def __init__(self, article_cache_service: ArticleCacheService):
        self.article_cache_service = article_cache_service

    async def _get_or_create_tags(self, tag_names, user: User):
        tags = []
        if tag_names:
            lower_tag_names = set()
            tag_name_pairs = []

            for origin_tag_name in tag_names:
                lower_tag_name = origin_tag_name.strip().lower()
                if lower_tag_name not in lower_tag_names:
                    lower_tag_names.add(lower_tag_name)
                    tag_name_pairs.append((origin_tag_name.strip(), lower_tag_name))
            for origin_name, lower_name in tag_name_pairs:
                tag = await Tag.get_or_none(name__iexact=lower_name, is_deleted=False, user=user)
                if not tag:
                    tag = await Tag.create(name=origin_name, user=user)
                tags.append(tag)
        return tags

    async def create(self, param: ArticleCreateParam, user: User) -> bool:
        # 检测文章是否已经存在
        article = await Article.get_or_none(title=param.title, is_deleted=False, user=user)
        if article:
            raise BlogException(BlogErrorEnum.ARTICLE_EXIST)
        # 检测分类是否存在
        category = await Category.get_or_none(pk=param.category_id, is_deleted=False, user=user)
        if not category:
            raise BlogException(BlogErrorEnum.CATEGORY_NOT_FOUND)
        # 检测并创建标签
        tags = await self._get_or_create_tags(param.tag_names, user)

        async with in_transaction():
            article = Article()
            article.title = param.title
            article.intro = param.intro
            article.content = param.content
            article.seo_title = param.seo_title
            article.seo_keywords = param.seo_keywords
            article.seo_description = param.seo_description
            article.category = category
            article.user = user
            await article.save()

            if tags:
                await article.tags.add(*tags)

            # 更新缓存
            await self.article_cache_service.update_article_by_id(article.pk)

        return True

    async def update(self, param: ArticleUpdateParam, user: User):
        # 检测文章是否存在
        article = await Article.get_or_none(pk=param.id, is_deleted=False, user=user)
        if not article:
            raise BlogException(BlogErrorEnum.ARTICLE_NOT_FOUND)
        # 检测分类是否存在
        category = await Category.get_or_none(pk=param.category_id, is_deleted=False, user=user)
        if not category:
            raise BlogException(BlogErrorEnum.CATEGORY_NOT_FOUND)

        # 检测并创建标签
        tags = await self._get_or_create_tags(param.tag_names, user)

        @atomic()
        async def save_article():
            # 更新文章
            article.title = param.title
            article.intro = param.intro
            article.content = param.content
            article.seo_title = param.seo_title
            article.seo_keywords = param.seo_keywords
            article.seo_description = param.seo_description
            article.category = category
            await article.save()
            # 清除历史标签关联数据
            await article.tags.clear()
            if tags:
                await article.tags.add(*tags)

        await save_article()

        # 更新缓存
        await self.article_cache_service.update_article_by_id(param.id)

        return True

    async def delete(self, param: IdParam, user: User) -> bool:
        await Article.filter(pk=param.id, is_deleted=False, user=user).update(is_deleted=True)
        await self.article_cache_service.delete_article_by_id(param.id)
        return True

    async def page_list(self, param: ArticlePageParam, user: User):
        queryset = Article.filter(is_deleted=False, user=user).order_by('-id').prefetch_related('category', 'tags')
        if param.title:
            queryset = queryset.filter(title__icontains=param.title)
        if param.category_id:
            queryset = queryset.filter(category__id=param.category_id)
        if param.tag_id:
            queryset = queryset.filter(tags__id=param.tag_id)

        count = await queryset.count()
        articles = []
        if  count > 0:
            articles = await queryset.offset( (param.page - 1) * param.page_size ).limit(param.page_size).all()
        result_list = [ArticlePageItemResult.model_validate(article) for article in articles]

        return ApiPageResult.success(param.page, param.page_size, count, result_list)

    async def update_status(self, param: ArticleUpdateStatusParam, user: User) -> bool:
        # 检测文章是否存在
        article = await Article.get_or_none(pk=param.id, is_deleted=False, user=user)
        if not article:
            raise BlogException(BlogErrorEnum.ARTICLE_NOT_FOUND)
        if article.status == param.status:
            return True
        article.status = param.status
        article.updated_at = datetime.now()
        await article.save(update_fields=['status', 'updated_at'])
        # 更新缓存
        await self.article_cache_service.update_article_by_id(param.id)
        return True

    async def get_by_id(self, article_id: int, user: User) -> ArticleDetailResult:
        article = await Article.get_or_none(pk=article_id, is_deleted=False, user=user).prefetch_related('category', 'tags')
        if not article:
            raise BlogException(BlogErrorEnum.ARTICLE_NOT_FOUND)
        return ArticleDetailResult.model_validate(article)