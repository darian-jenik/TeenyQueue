# routes/__init__.py

from fastapi import APIRouter

from .queue_routes import test_queue_router

api_router = APIRouter()
api_router.include_router(test_queue_router)

# end
