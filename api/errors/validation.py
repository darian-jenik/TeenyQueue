# api/errors/validation.py

from api import app
from config import log

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    log.warning(f"Invalid data from endpoint: {request.url.path}, {exc}")
    # TODO: add await for a better solution, see below.
    return JSONResponse(
        status_code=422,
        content={
            "message": "Validation error",
            "errors": exc.errors(),
            "path": request.url.path,
            "method": request.method
        },
    )

# end
