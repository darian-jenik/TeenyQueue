# api/db/models.py

from sqlalchemy import Column, String, DateTime, UUID, Boolean
from sqlalchemy.types import TypeDecorator, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import DeclarativeBase


import json
import base64
import uuid


class Base(DeclarativeBase):
    pass


class Base64EncodedText(TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        return base64.b64encode(json.dumps(value).encode()).decode()

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        return json.loads(base64.b64decode(value.encode()).decode())


class QueueDBModel(Base):
    __tablename__ = 'queue'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    pub_module_name = Column(String, nullable=False)
    topic = Column(String, nullable=False)
    message_body = Column(Base64EncodedText, nullable=False)
    _authentication_key = Column(String, nullable=True)
    has_authentication = Column(Boolean, default=False, nullable=False)
    target_module_name = Column(String, nullable=True)
    received_at = Column(DateTime(timezone=True), server_default=func.now())
    delivered_at = Column(DateTime(timezone=True), nullable=True)
    schedule_date = Column(DateTime(timezone=True), nullable=True)
    delivered_to_module = Column(String, nullable=True)

# end
