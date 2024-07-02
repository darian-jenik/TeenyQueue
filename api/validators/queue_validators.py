# api/validators/queue_validators.py

from pydantic import BaseModel, Field, field_validator, UUID4, ConfigDict, FutureDatetime
from typing import Optional, Dict, Any
import uuid, re
from config import env

QUEUE_ALPHA_PATTERN: re.Pattern = re.compile(r'^[\w\-]+$')


class PaginationParams(BaseModel):
    page_size: Optional[int] = env.config.get('default_page_size', 1000)
    page_number: Optional[int] = 1


class PublishQueue(BaseModel):
    pub_module_name: str = Field(..., description="The name of the publisher module.  [a-z][A-Z][0-9][-_]")
    topic: str = Field(..., description="The name of the queue.  [a-z][A-Z][0-9][-_]")
    message_body: Dict[str, Any] = Field(..., description="The JSON message_body or {}")
    authentication_key: Optional[UUID4] = Field(None, description="Optional or Valid UUID4.")
    target_module_name: Optional[str] = Field(None, description="An optional target module name. [a-z][A-Z][0-9][-_]")
    schedule_date: Optional[FutureDatetime] = Field(None, description="Datetime in the future to be published.")

    model_config = ConfigDict(extra='forbid')

    @field_validator('authentication_key')
    def validate_authentication_key(cls, value):
        if not isinstance(value, uuid.UUID) or value.version != 4:
            raise ValueError('authentication_key must be a valid UUID4')
        return value

    @field_validator('pub_module_name', 'topic', 'target_module_name')
    def validate_string_fields(cls, value, field):
        if value is not None:
            if len(value) > 30:
                raise ValueError(f'{field.field_name} must be no more than 30 characters long')
            if not QUEUE_ALPHA_PATTERN.match(value):
                raise ValueError(f'{field.field_name} must be alphanumeric and can include _ and -')
        return value


class QueueQuery(BaseModel):
    pub_module_name: Optional[str] = Field(None, description="An optional target module name. [a-z][A-Z][0-9][-_]")
    topic: Optional[str] = Field(None, description="An optional target module name. [a-z][A-Z][0-9][-_]")
    target_module_name: Optional[str] = Field(None, description="An optional target module name. [a-z][A-Z][0-9][-_]")
    delivered_at: Optional[bool] = Field(None, description="If entries have been surbscribed (True) or waiting to be subscribed (False).")

    model_config = ConfigDict(extra='forbid')

    @field_validator('pub_module_name', 'topic', 'target_module_name')
    def validate_string_fields(cls, value, field):
        if value is not None:
            if len(value) > 30:
                raise ValueError(f'{field.field_name} must be no more than 30 characters long')
            if not QUEUE_ALPHA_PATTERN.match(value):
                raise ValueError(f'{field.field_name} must be alphanumeric and can include _ and -')
        return value


class SubscribeQueue(BaseModel):
    sub_module_name: str = Field(..., description="The name of the publisher module.  [a-z][A-Z][0-9][-_]")
    topic: str = Field(..., description="The name of the queue.  [a-z][A-Z][0-9][-_]")
    authentication_key: Optional[UUID4] = Field(None, description="Optional or Valid UUID4.")
    target_module_name: Optional[str] = Field(None, description="An optional target module name. [a-z][A-Z][0-9][-_]")

    model_config = ConfigDict(extra='forbid')

    @field_validator('authentication_key')
    def validate_authentication_key(cls, value):
        if not isinstance(value, uuid.UUID) or value.version != 4:
            raise ValueError('authentication_key must be a valid UUID4')
        return value

    @field_validator('sub_module_name', 'topic')
    def validate_string_fields(cls, value, field):
        if value is not None:
            if len(value) > 30:
                raise ValueError(f'{field.field_name} must be no more than 30 characters long')
            if not QUEUE_ALPHA_PATTERN.match(value):
                raise ValueError(f'{field.field_name} must be alphanumeric and can include _ and -')
        return value

# end
