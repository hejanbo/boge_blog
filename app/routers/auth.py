from typing import Annotated
from urllib import response

from fastapi import APIRouter, Depends
from fastapi.params import Query
from pydantic import EmailStr

from app.core import deps
from app.models import User
from app.schemas.auth import RegisterParam, LoginParam, RefreshTokenParam, LoginResult
from app.schemas.common import ApiResult
from app.services.auth import AuthService

router = APIRouter(tags=["用户认证"])

@router.get("/get_verify_code", response_model=ApiResult[bool])
async def get_verify_code(email: Annotated[EmailStr, Query()],
                          auth_service: Annotated[AuthService, Depends(deps.get_auth_service)]):
    return ApiResult.success(await auth_service.send_verify_code(email))

@router.post("/register", response_model=ApiResult[bool])
async def register(param: RegisterParam,
                          auth_service: Annotated[AuthService, Depends(deps.get_auth_service)]):
    return ApiResult.success(await auth_service.register(param))

@router.post("/login", response_model=ApiResult[LoginResult])
async def login(param: LoginParam,
                auth_service: Annotated[AuthService, Depends(deps.get_auth_service)]):
    return ApiResult.success(await auth_service.login(param))

@router.get("/test", dependencies=[Depends(deps.check_permission("test2"))])
async def test(user: Annotated[User, Depends(deps.get_current_user)]):
    return user.email

@router.post("/refresh_token", response_model=ApiResult[LoginResult])
async def refresh_token(param: RefreshTokenParam,
                auth_service: Annotated[AuthService, Depends(deps.get_auth_service)]):
    return ApiResult.success(await auth_service.refresh_token(param))