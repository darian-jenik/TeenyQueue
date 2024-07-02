# app/errors/generic.py

from api import app
from config import log

from fastapi.exception_handlers import http_exception_handler
from starlette.exceptions import HTTPException as StarletteHTTPException


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    log.warning(f"An HTTP error occurred: {repr(exc)}")
    return await http_exception_handler(request, exc)

# end
