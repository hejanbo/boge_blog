import asyncio
import logging
from typing import List

from app.cache.articles import ArticleCacheService
from app.core.caches import article_view_count_cache
from app.core.enums import ArticleStatusEnum, BlogErrorEnum
from app.core.exceptions import BlogException
from app.models import Article
from app.schemas.articles import ArticlePageItemResult, ArticleDetailResult, ArticlePageParam
from app.schemas.common import BasePageParam, ApiPageResult

LATEST_ARTICLE_LOCK = asyncio.Lock()


ARTICLE_GLOBAL_LOCK = asyncio.Lock()


class ArticleService:

    def __init__(self, article_cache_service: ArticleCacheService):
        self.article_cache_service = article_cache_service

    async def page_latest_articles(self, param: BasePageParam) -> ApiPageResult[List[ArticlePageItemResult]]:
        # 先从缓存中获取
        cache_key = f'latest:{param.page}:{param.page_size}'
        result = await self.article_cache_service.page_list(cache_key, param.page, param.page_size)
        if result:
            return result

        # 缓存中没有, 从db中获取
        queryset = Article.filter(is_deleted=False, status=ArticleStatusEnum.PUBLISHED).prefetch_related('category', 'tags').order_by('-id')
        count = await queryset.count()
        articles = []
        if count > 0:
            articles = await queryset.offset((param.page - 1) * param.page_size).limit(param.page_size).all()
        result_list = [ArticlePageItemResult.model_validate(article) for article in articles]
        ids = [article.id for article in articles]


        result = ApiPageResult.success(param.page, param.page_size, count, result_list)

        # 将结果放入缓存
        await self.article_cache_service.page_list_set(cache_key, count, ids)

        return result

    async def get_by_id(self, article_id: int) -> ArticleDetailResult:
        article = await self.article_cache_service.get_article_by_id(article_id)
        if not article:
            raise BlogException(BlogErrorEnum.ARTICLE_NOT_FOUND)
        # 记录访问次数到缓存
        view_count = article_view_count_cache.get(article_id)
        if not view_count:
            view_count = 0
        view_count = view_count + 1
        article_view_count_cache.set(article_id, view_count)

        return ArticleDetailResult.model_validate(article)


    async def page_list(self, param: ArticlePageParam) -> ApiPageResult[List[ArticlePageItemResult]]:
        # 先从缓存中获取
        cache_key = f'page:{param.page}:{param.page_size}:{param.title}:{param.tag_id}:{param.category_id}'
        logging.debug(f'cache_key: {cache_key}')
        result = await self.article_cache_service.page_list(cache_key, param.page, param.page_size)
        if result:
            return result

        # 从db中获取
        queryset = Article.filter(is_deleted=False, status=ArticleStatusEnum.PUBLISHED).prefetch_related('category', 'tags').order_by('-id')
        if param.category_id:
            queryset = queryset.filter(category__id=param.category_id)
        if param.tag_id:
            queryset = queryset.filter(tags__id=param.tag_id)
        if param.title:
            queryset = queryset.filter(title__icontains=param.title)
        count = await queryset.count()
        articles = []
        if count > 0:
            articles = await queryset.offset((param.page - 1) * param.page_size).limit(param.page_size).all()
        result_list = [ArticlePageItemResult.model_validate(article) for article in articles]

        ids = [article.id for article in articles]
        # 将结果放入缓存
        await self.article_cache_service.page_list_set(cache_key, count, ids)

        return ApiPageResult.success(param.page, param.page_size, count, result_list)