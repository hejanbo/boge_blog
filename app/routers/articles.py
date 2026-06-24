from typing import Annotated, List
from loguru import logger

from fastapi import APIRouter
from fastapi.params import Query, Depends, Path

from app.core import deps
from app.schemas.articles import ArticlePageParam, ArticlePageItemResult, ArticleDetailResult
from app.schemas.common import BasePageParam, ApiResult, ApiPageResult
from app.services.articles import ArticleService

router = APIRouter(prefix="/articles", tags=['文章相关接口'])

@router.get("/latest", response_model=ApiPageResult[List[ArticlePageItemResult]])
async def page_latest_articles(param: Annotated[BasePageParam, Query()],
                               article_service: Annotated[ArticleService, Depends(deps.get_article_service)]):
    """
    分页查询文章
    """

    logger.info(f"test loguru logger 1111122222")

    return await article_service.page_latest_articles(param)

@router.get("/page_list", response_model=ApiPageResult[List[ArticlePageItemResult]])
async def page_list(param: Annotated[ArticlePageParam, Query()],
                               article_service: Annotated[ArticleService, Depends(deps.get_article_service)]):
    """
    获取最新文章
    """
    return await article_service.page_list(param)

@router.get("/{article_id}", response_model=ApiResult[ArticleDetailResult])
async def get_by_id(article_id: Annotated[int, Path()],
                    article_service: Annotated[ArticleService, Depends(deps.get_article_service)]):
    return ApiResult.success(await article_service.get_by_id(article_id))