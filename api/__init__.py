# api/__init__.py

try:

    from fastapi import FastAPI, HTTPException, Request
    import os
    from contextlib import asynccontextmanager
    from .db.core import sessionmanager, get_conn_string
    from config import env, log

    sessionmanager.init(get_conn_string('queue'))

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        yield
        if sessionmanager._engine is not None:
            await sessionmanager.close()

    if env.DEBUG:
        app = FastAPI(lifespan=lifespan)
    else:
        app = FastAPI(
            docs_url=env.DEBUG,
            redoc_url=env.DEBUG,
            lifespan=lifespan
        )

    from .routers import api_router
    app.include_router(api_router)

    # #############################################################################
    @app.on_event("startup")
    async def startup_event():
        # this needs to be configured at this time after uvicorn starts.
        env.add_wsgi_uvicorn_logging()
        log.debug(f'WSGI uvicorn logging enabled for module: {os.environ.get("MODULE_NAME", "UNNAMED_MODULE")}')

    # #############################################################################
    @app.get("/", include_in_schema=False)
    async def root():
        """
        Use this for the health check.
        """
        raise HTTPException(status_code=200, detail="Server is running.")

    # #############################################################################
    @app.middleware("http")
    async def log_middleware(request: Request, call_next):
        log.debug(f"Request: {request.url.path} {request.method}")
        response = await call_next(request)
        return response

except Exception as e:
    print(f'EXCEPTION STARTING APP: {e}')

# end
