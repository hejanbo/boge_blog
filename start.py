from app.core.config import settings

if __name__ == "__main__":
    import uvicorn

    reload = True if settings.ENV == 'dev' else False

    uvicorn.run("app.main:myapp", host=settings.SERVER_HOST, port=settings.SERVER_PORT, reload=reload)