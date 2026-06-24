import logging

from loguru import logger

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from tortoise.contrib.fastapi import register_tortoise

from app.core import config, exceptions, lifespans

logging.basicConfig(level=logging.DEBUG)

from app.routers import auth, admin, articles, categories, tags

logger.add("logs/app.log", rotation="10 MB", retention=5, level="INFO")

myapp = FastAPI(lifespan=lifespans.lifespan)

register_tortoise(myapp, config=config.TORTOISE_ORM, generate_schemas=False)

myapp.include_router(auth.router, prefix="/api")
myapp.include_router(articles.router, prefix="/api")
myapp.include_router(categories.router, prefix="/api")
myapp.include_router(tags.router, prefix="/api")
myapp.include_router(admin.admin_router, prefix="/api")


# 注册异常
myapp.add_exception_handler(exceptions.BlogException, exceptions.blog_exception_handler) # type: ignore
myapp.add_exception_handler(RequestValidationError, exceptions.validation_exception_handler) # type: ignore
myapp.add_exception_handler(Exception, exceptions.global_exception_handler)

@myapp.get("/")
async def root():
    return {"message": "Hello World"}