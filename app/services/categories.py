import asyncio

from tortoise.expressions import Q
from tortoise.functions import Count

from app.core.caches import stat_cache, load_cache_with_lock
from app.core.enums import ArticleStatusEnum
from app.models import Category
from app.schemas.categories import CategoryStatResult

CATEGORY_STAT_LOCK = asyncio.Lock()


class CategoryService:

    async def stat_categories(self) -> list[CategoryStatResult]:
        # 先从缓存中获取
        cache_key = "category_stat"

        async def _fetch_from_db():
            # 从db中获取
            categories = await (Category.filter(is_deleted=False).order_by('-id')
                                .annotate(published_article_count=
                                          Count("articles",
                                                _filter=Q(articles__status=ArticleStatusEnum.PUBLISHED,
                                                          articles__is_deleted=False)))
                                .filter(published_article_count__gt=0)
                                .values("id", "name", "published_article_count"))
            return [CategoryStatResult.model_validate(category) for category in categories]
        return await load_cache_with_lock(cache_key, stat_cache, CATEGORY_STAT_LOCK, _fetch_from_db)