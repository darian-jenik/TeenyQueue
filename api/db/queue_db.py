# api/db/queue_dv.py

from sqlalchemy import and_, delete, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from sqlalchemy.future import select
from sqlalchemy.orm import class_mapper
from api.validators.queue_validators import PaginationParams

import asyncio
from datetime import datetime
from typing import Optional

import bcrypt

from .models import QueueDBModel

from api.validators import QueueQuery, SubscribeQueue, PublishQueue


def row_to_dict(row, fields):
    return {field: getattr(row, field) for field in fields}


class QueueDB(QueueDBModel):

    @property
    def authentication_key(self):
        return self._authentication_key

    @authentication_key.setter
    def authentication_key(self, value):
        if value:
            # Salt and hash the authentication key
            salt = bcrypt.gensalt()
            hashed_key = bcrypt.hashpw(str(value).encode('utf-8'), salt)
            self._authentication_key = hashed_key.decode('utf-8')
            self.has_authentication = True
        else:
            self._authentication_key = None

    @classmethod
    async def message_response(cls, message=None, message_body=False) -> dict:

        response = {k: v for k, v in message.items() if v is not None}

        if '_authentication_key' in response.keys():
            del response['_authentication_key']

        if not message_body:
            del response['message_body']

        return response


    # TODO: check why this is not being called, but fukit, it work via the setter above.
    # @validates('authentication_key')
    # def validate_authentication_key(self, key, value):
    #     # This will be called whenever the authentication_key is set
    #     print(f"Setting authentication_key to {value} {key}")
    #     self.authentication_key = value
    #     return self._authentication_key

    @classmethod
    async def pub(cls, db: AsyncSession, queue_data: PublishQueue, **kwargs):

        message = cls(**queue_data.dict())
        db.add(message)
        await db.commit()
        await db.refresh(message)

        return await cls.message_response(message.__dict__, message_body=True)

    @classmethod
    async def sub(cls, db: AsyncSession, sub_query: SubscribeQueue) -> Optional[dict]:
        try:

            conditions = [
                cls.topic == sub_query.topic,
                cls.delivered_at == None
            ]

            if db.bind.dialect.name == 'postgresql':
                # current_time_utc = func.timezone('UTC', func.now()) # TODO, fix this.  I ran out of patience.
                current_time_utc = func.now()
            else:
                current_time_utc = func.now()  # SQLite does not support timezone but is used in the tests.

            conditions.append(
                or_(
                    cls.schedule_date == None,
                    current_time_utc > cls.schedule_date
                )
            )

            # if sub_query.target_module_name is specified ONLY pickup messages specified for myself and ignore all others
            if sub_query.target_module_name:
                conditions.append(cls.target_module_name == sub_query.sub_module_name)
            else:
                conditions.append(
                    or_(
                        cls.target_module_name == None,
                        cls.target_module_name == sub_query.sub_module_name
                    )
                )

            # # if the query has not supplied an authentication key then ignore messages with one
            if sub_query.authentication_key is None:
                conditions.append(cls._authentication_key == None)

            result = await db.execute(
                select(cls)
                .filter(and_(*conditions))
                .order_by(cls.received_at.asc())
                .with_for_update()
            )

            queue_items = result.scalars().all()

            for message in queue_items:

                # check this didn't get updated while we were waiting on the lock
                if message.delivered_at is not None:
                    continue

                # Note: I'm not worried about enumerating the authentication keys as using UUID4 makes the key space too large to make it an issue.
                if message.authentication_key is not None and sub_query.authentication_key is not None:
                    if not bcrypt.checkpw(str(sub_query.authentication_key).encode('utf-8'), message.authentication_key.encode('utf-8')):
                        continue

                message.delivered_at = datetime.now()
                message.delivered_to_module = sub_query.sub_module_name

                data = {
                    'topic': message.topic,
                    'message_body': message.message_body
                }
                if message.schedule_date is not None:
                    data['schedule_date'] = message.schedule_date.isoformat()

                await db.commit()
                await db.refresh(message)
                return await cls.message_response(message=message.__dict__, message_body=True)

            await db.rollback()

        except Exception as e:
            await db.rollback()
            print(f"Process {asyncio.current_task().get_name()} failed to acquire lock, got exception {e}")
            return None

    @classmethod
    async def list(cls, db: AsyncSession, queue_query: QueueQuery, pagination: PaginationParams):

        conditions = []

        if queue_query.pub_module_name is not None:
            conditions.append(cls.pub_module_name == queue_query.pub_module_name)

        if queue_query.topic is not None:
            conditions.append(cls.topic == queue_query.topic)

        if queue_query.target_module_name is not None:
            conditions.append(cls.target_module_name == queue_query.target_module_name)

        if queue_query.delivered_at is not None:
            if queue_query.delivered_at is True:
                conditions.append(cls.delivered_at != None)
            else:
                conditions.append(cls.delivered_at == None)

        total_count_query = select(func.count()).where(and_(*conditions))
        total_count_result = await db.execute(total_count_query)
        total_count = total_count_result.scalar_one()

        offset = (pagination.page_number - 1) * pagination.page_size

        query = select(cls).where(and_(*conditions)).limit(pagination.page_size).offset(offset)
        result = await db.execute(query)
        rows = result.scalars().all()

        messages = []
        for row in rows:
            message = {c.key: getattr(row, c.key) for c in class_mapper(row.__class__).columns}
            clean_message = {k: v for k, v in message.items() if v is not None}

            if '_authentication_key' in clean_message.keys():
                del clean_message['_authentication_key']

            if 'message_body' in clean_message.keys():
                del clean_message['message_body']

            if 'has_authentication' in clean_message.keys() and clean_message['has_authentication'] is False:
                del clean_message['has_authentication']

            messages.append(clean_message)

        return total_count, pagination.page_size, pagination.page_number, messages

    @classmethod
    async def list_all(cls, db: AsyncSession, pagination: PaginationParams):

        result = await db.execute(select(func.count()).select_from(cls))
        total_count = result.scalar_one()

        offset = (pagination.page_number - 1) * pagination.page_size
        query = select(cls).limit(pagination.page_size).offset(offset)
        result = await db.execute(query)
        rows = result.scalars().all()

        messages = []
        for row in rows:
            message = {c.key: getattr(row, c.key) for c in class_mapper(row.__class__).columns}
            clean_message = {k: v for k, v in message.items() if v is not None}

            if '_authentication_key' in clean_message.keys():
                del clean_message['_authentication_key']

            if 'message_body' in clean_message.keys():
                del clean_message['message_body']

            if 'has_authentication' in clean_message.keys() and clean_message['has_authentication'] is False:
                del clean_message['has_authentication']

            messages.append(clean_message)

        return total_count, pagination.page_size, pagination.page_number, messages

    @classmethod
    async def delete_delivered(cls, db: AsyncSession):
        result = await db.execute(select(func.count()).select_from(cls).where(cls.delivered_at.isnot(None)))
        count = result.scalar_one()

        await db.execute(delete(cls).where(cls.delivered_at.isnot(None)))
        await db.commit()

        return count

    @classmethod
    async def delete_all(cls, db: AsyncSession):
        result = await db.execute(select(func.count()).select_from(cls))

        count = result.scalar_one()

        await db.execute(delete(cls))
        await db.commit()

        return count

# end
