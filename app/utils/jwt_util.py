import base64
from datetime import datetime, UTC, timedelta
from typing import Any
from uuid import uuid4

import jwt
from fastapi import HTTPException

from app.core.config import Settings, settings


def create_token(body: dict[str, Any]):
    return jwt.encode(body, str(uuid4()), algorithm="HS256")

def create_access_token(body: dict[str, Any]) -> str:
    payload = body.copy()

    now = datetime.now(UTC)

    payload.update({
        "iss": settings.JWT_ISS,
        "aud": settings.JWT_AUD,
        "exp": now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
        "nbf": now,
        "iat": now,
        "jti": str(uuid4()),
        "typ": "access"
    })

    return jwt.encode(payload, settings.SECURITY_KEY, algorithm="HS256")

def create_refresh_token(body: dict[str, Any]) -> str:
    payload = body.copy()

    now = datetime.now(UTC)

    payload.update({
        "iss": settings.JWT_ISS,
        "aud": settings.JWT_AUD,
        "exp": now + timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES),
        "nbf": now,
        "iat": now,
        "jti": str(uuid4()),
        "typ": "refresh"
    })

    return jwt.encode(payload, settings.SECURITY_KEY, algorithm="HS256")

def verify_token(token: str, token_type: str = 'access') -> dict[str, Any]:
    payload = jwt.decode(token, settings.SECURITY_KEY, algorithms=["HS256"], audience=settings.JWT_AUD, issuer=settings.JWT_ISS)
    if not payload:
        raise HTTPException(status_code=401, detail="无效的token")
    if payload.get("typ") != token_type:
        raise HTTPException(status_code=401, detail="无效的token")
    return payload

if __name__ == "__main__":
    print(str(uuid4()))
    # now = datetime.now(UTC)
    #
    # body = {
    #     "iss": "bogeblog",
    #     "sub": "1",
    #     "aud": "android",
    #     "exp": now + timedelta(days=1),
    #     "nbf": now,
    #     "iat": now,
    #     "jti": str(uuid4()),
    # }
    #
    # print(create_token(body))

    # token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJib2dlYmxvZyIsInN1YiI6IjEiLCJhdWQiOiJhbmRyb2lkIiwiZXhwIjoxNzc4MjExNjk2LCJuYmYiOjE3NzgxMjUyOTYsImlhdCI6MTc3ODEyNTI5NiwianRpIjoiNTM0MzE1MjgtOThjYi00Mjg5LWFhNjctMDg3ZjZmMjZkNTlmIn0.1tc9OvyexYE3I-XIXJK3FqoFKXS_JU0Mkosg-oosnf4"
    # header, payload, signature = token.split( ".")
    #
    # print(base64.urlsafe_b64decode(header))
    # payload = payload + "="
    # print(len(payload))
    #
    # print(base64.urlsafe_b64decode(payload))
