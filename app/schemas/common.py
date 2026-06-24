import math
from typing import TypeVar, Generic

from pydantic import BaseModel, Field

T = TypeVar("T")


class IdParam(BaseModel):
    id: int

class BasePageParam(BaseModel):
    page: int = Field(1, description="页码")
    page_size: int = Field(10, description="每页数量")

class ApiResult(BaseModel, Generic[T]):
    code: int = 200
    msg: str = "success"
    data: T | None = None

    @staticmethod
    def success(data: T | None = None):
        return ApiResult(data=data)

    @staticmethod
    def fail(message: str, code: int = 500):
        return ApiResult(code=code, msg=message, data=None)


class ApiPageResult(BaseModel, Generic[T]):
    code: int = 200
    msg: str = "success"
    data: T | None = None

    page: int = Field(1, description="页码")
    page_size: int = Field(10, description="每页数量")
    total: int = Field(0, description="总条数")
    total_pages: int = Field(0, description="总页数")

    @staticmethod
    def success(page: int, page_size: int, total: int, data: T | None = None):
        if page_size == 0 or total == 0:
            total_pages = 0
        else:
            total_pages = math.ceil(total / page_size)

        return ApiPageResult(data=data, page=page, page_size=page_size, total=total, total_pages=total_pages)

    @staticmethod
    def fail(message: str, code: int = 500):
        return ApiPageResult(code=code, msg=message, data=None)