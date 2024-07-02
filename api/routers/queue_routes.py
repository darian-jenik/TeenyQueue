# api/routes/queue_routes.py

from fastapi import APIRouter, HTTPException
from fastapi_restful.cbv import cbv
from api.validators import PublishQueue, QueueQuery, SubscribeQueue
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.params import Depends
from api.db.core import get_db
from api.db.queue_db import QueueDB
from sqlalchemy.exc import InterfaceError, OperationalError
from functools import wraps
from typing import Optional
from api.validators.queue_validators import PaginationParams

from config import env, log


# test_queue_router = APIRouter(prefix="/v1")
# Let's not get ambitious.
test_queue_router = APIRouter()


def http_exception_handler(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except (InterfaceError, OperationalError) as e:
            log.critical(f"InterfaceError or OperationalError in {func.__name__}: {e}")
            raise HTTPException(status_code=500, detail=f"Internal Server Error in {func.__name__}: {e.code=} {e}")
        except Exception as e:
            log.critical(f"Exception in {func.__name__}: {e}")
            if isinstance(e, HTTPException):
                raise e
            raise HTTPException(status_code=500, detail=f"Internal Server Error in {func.__name__}: {e}")
    return wrapper


@cbv(test_queue_router)
class TestQueue:

    @test_queue_router.post("/pub")
    @http_exception_handler
    async def pub_queue_data(self, queue_data: PublishQueue, db: AsyncSession = Depends(get_db)):

        message = await QueueDB.pub(db, queue_data)

        return {"message": f"Queue entry published.", "data": message}

    @test_queue_router.post("/sub")
    @http_exception_handler
    async def sub_queue_data(self, sub_data: SubscribeQueue, db: AsyncSession = Depends(get_db)):

        message = await QueueDB.sub(db, sub_data)

        if message is not None:
            return {"message": f"Message available.", "data": message}

        else:
            raise HTTPException(status_code=404, detail=f"No messages.")

    @test_queue_router.get("/list_all")
    @http_exception_handler
    async def list_all_queue_data(self, db: AsyncSession = Depends(get_db), pagination: Optional[PaginationParams] = Depends(PaginationParams)):

        total_count, page_size, page_number, messages = await QueueDB.list_all(db, pagination)

        return {"total_count": total_count, "page_size": page_size, "page_number": page_number, "messages": messages}

    @test_queue_router.post("/list")
    @http_exception_handler
    async def list_queue_data(self, query_data: QueueQuery, db: AsyncSession = Depends(get_db), pagination: Optional[PaginationParams] = Depends(PaginationParams)):

        total_count, page_size, page_number, messages = await QueueDB.list(db, query_data, pagination)

        return {"total_count": total_count, "page_size": page_size, "page_number": page_number, "messages": messages}

    @test_queue_router.delete("/delete_delivered")
    @http_exception_handler
    async def delete_delivered(self, db: AsyncSession = Depends(get_db)):

        count = await QueueDB.delete_delivered(db)

        return {"message": f"Deleted {count} delivered messages."}

    @test_queue_router.delete("/delete_all")
    @http_exception_handler
    async def delete_all(self, db: AsyncSession = Depends(get_db)):

        count = await QueueDB.delete_all(db)

        return {"message": f"Deleted {count} messages."}

# end
