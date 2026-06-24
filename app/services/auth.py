import asyncio
import random
from datetime import timedelta, datetime

from fastapi import HTTPException
from tortoise import Model

from app.core.caches import verify_code_cache
from app.core.config import Settings, settings
from app.core.enums import BlogErrorEnum
from app.core.exceptions import BlogException
from app.models import User
from app.schemas.auth import RegisterParam, LoginParam, LoginResult, RefreshTokenParam
from app.utils import smtp_util, pwd_util, jwt_util

EMAIL_LOCKS = {}

VERIFY_CODE_LOCK = asyncio.Lock()

class AuthService:

    async def send_verify_code(self, email: str) -> bool:

        if email not in EMAIL_LOCKS:
            async with VERIFY_CODE_LOCK:
                if email not in EMAIL_LOCKS:
                    EMAIL_LOCKS[email] = asyncio.Lock()

        async with EMAIL_LOCKS[email]:
            verify_code_dict = verify_code_cache.get(email)
            if verify_code_dict:
                one_minutes = timedelta(minutes=1)
                if verify_code_dict.get("created_at") + one_minutes > datetime.now():
                    raise HTTPException(status_code=400, detail="验证码已发送，请稍后再试")
            code = ''.join(random.choices('0123456789', k=6))
            now = datetime.now()
            verify_code_cache.set(email, {
                'code': code,
                'created_at': now
            })
            try:
                smtp_util.send_message(f'你的注册验证码是: {code}, 将在3分钟后过期!', email, "注册验证码")
            except Exception as e:
                print(e)
                raise BlogException(BlogErrorEnum.SYSTEM_ERROR)
            return True

    async def register(self, param: RegisterParam) -> bool:
        verify_code_dict = verify_code_cache.get(param.email)
        if not verify_code_dict:
            raise BlogException(BlogErrorEnum.VERIFY_CODE_EXPIRED)
        if verify_code_dict.get("code") != param.code:
            raise BlogException(BlogErrorEnum.VERIFY_CODE_EXPIRED_OR_INVALID)
        user = await User.get_or_none(email=param.email, is_deleted=False)
        if user:
            raise BlogException(BlogErrorEnum.USER_EXISTS)
        hashed_password = pwd_util.get_password_hash(param.password)

        user_data = param.model_dump()
        user_data['password'] = hashed_password

        await User.create(**user_data)

        return True

    async def login(self, param: LoginParam) -> LoginResult:
        # 1. 将用户查询出来
        user = await User.get_or_none(email=param.email, is_deleted=False)
        if not user:
            raise BlogException(BlogErrorEnum.USER_NOT_FOUND_OR_PASSWORD_ERROR)
        # 2. 验证密码
        if not pwd_util.verify_password(param.password, user.password):
            raise BlogException(BlogErrorEnum.USER_NOT_FOUND_OR_PASSWORD_ERROR)
        # 3. 生成token
        user_data = {
            "sub": str(user.pk),
            "email": user.email
        }
        access_token = jwt_util.create_access_token(user_data)
        refresh_token = jwt_util.create_refresh_token(user_data)
        seconds = int(timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES).total_seconds())
        return LoginResult(access_token=access_token, refresh_token=refresh_token, expires_in=seconds, email=user.email)

    async def refresh_token(self, param: RefreshTokenParam) -> LoginResult:
        payload = jwt_util.verify_token(param.token, 'refresh')
        if not payload:
            raise BlogException(BlogErrorEnum.INVALID_TOKEN)
        sub = payload.get("sub")
        if not sub:
            raise BlogException(BlogErrorEnum.INVALID_TOKEN)
        user = await User.get_or_none(id=int(str(sub)), is_deleted=False)
        if not user:
            raise BlogException(BlogErrorEnum.USER_NOT_FOUND)
        user_data = {
            "sub": str(user.pk),
            "email": user.email
        }
        access_token = jwt_util.create_access_token(user_data)
        refresh_token = jwt_util.create_refresh_token(user_data)
        seconds = int(timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES).total_seconds())
        return LoginResult(access_token=access_token, refresh_token=refresh_token, expires_in=seconds)