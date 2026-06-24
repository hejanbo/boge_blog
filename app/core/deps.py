from typing import Annotated

from fastapi import HTTPException
from fastapi.params import Header, Depends
from jwt import ExpiredSignatureError

from app.cache.articles import ArticleCacheService
from app.core.enums import BlogErrorEnum
from app.core.exceptions import BlogException
from app.models import User
from app.services.admin.categories import CategoryAdminService
from app.services.admin.tags import TagAdminService
from app.services.admin.articles import ArticleAdminService
from app.services.articles import ArticleService
from app.services.categories import CategoryService
from app.services.tags import TagService
from app.services.auth import AuthService
from app.utils import jwt_util


def get_article_cache_service() -> ArticleCacheService:
    return ArticleCacheService()

def get_auth_service() -> AuthService:
    return AuthService()

def get_category_admin_service() -> CategoryAdminService:
    return CategoryAdminService()

def get_tag_admin_service() -> TagAdminService:
    return TagAdminService()

def get_article_admin_service(article_cache_service: Annotated[ArticleCacheService, Depends(get_article_cache_service)]) -> ArticleAdminService:
    return ArticleAdminService(article_cache_service)



def get_article_service(article_cache_service: Annotated[ArticleCacheService, Depends(get_article_cache_service)]) -> ArticleService:
    return ArticleService(article_cache_service)

def get_category_service() -> CategoryService:
    return CategoryService()

def get_tag_service() -> TagService:
    return TagService()

async def get_current_user(authorization: Annotated[str, Header()]) -> User:
    parts = authorization.split(" ")
    print(parts)
    if parts[0] != 'Bearer' or len(parts) != 2:
        raise BlogException(BlogErrorEnum.ACCESS_TOKEN_INVALID)
    try:
        payload = jwt_util.verify_token(parts[1], 'access')
        sub = payload.get("sub")
        if not sub:
            raise BlogException(BlogErrorEnum.ACCESS_TOKEN_INVALID)
        user_id = int(str(sub))
        return await User.get(id=user_id)
    except ExpiredSignatureError:
        raise BlogException(BlogErrorEnum.ACCESS_TOKEN_EXPIRED)
    except Exception as e:
        raise BlogException(BlogErrorEnum.ACCESS_TOKEN_INVALID)

def check_permission(perm: str):
    def _check_permission(user: Annotated[User, Depends(get_current_user)]):
        if perm != 'test':
            raise HTTPException(status_code=401, detail="无权限")
    return _check_permission