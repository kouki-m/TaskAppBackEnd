from typing import Optional
import uuid
import datetime

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from app.schemas.base_schema import BaseSchema


class TaskCreateRequest(BaseSchema):
    title: str = Field(..., title="タスク名")
    description: Optional[str] = Field(None, title="タスクの説明")
    deadline: Optional[datetime.datetime] = Field(None, title="締め切り日時")
    # label: Optional[list[str]] = Field(
    #     None, title="ラベル", example=["Python", "FastAPI"]
    # )
    priority: Optional[str] = Field(None, title="優先度", example="High")
    status: Optional[str] = Field(None, title="ステータス", example="TODO")


class TaskCreateResponse(BaseSchema):
    id: uuid.UUID = Field(..., title="タスクID")
    message: str = Field(..., title="メッセージ")


class TaskListResponse(BaseSchema):
    id: uuid.UUID = Field(..., title="タスクID")
    title: str = Field(..., title="タスク名")
    description: Optional[str] = Field(None, title="タスクの説明")
    deadline: Optional[datetime.datetime] = Field(None, title="締め切り日時")
    # label: Optional[list[str]] = Field(None, title="ラベル")
    priority: Optional[str] = Field(None, title="優先度")
    status: Optional[str] = Field(None, title="ステータス")


class TaskDeleteResponse(BaseSchema):
    id: uuid.UUID = Field(..., title="タスクID")
    message: str = Field(..., title="メッセージ")


class TaskUpdateRequest(BaseSchema):
    title: Optional[str] = Field(None, title="タスク名")
    description: Optional[str] = Field(None, title="タスクの説明")
    deadline: Optional[datetime.datetime] = Field(None, title="締め切り日時")
    # label: Optional[list[str]] = Field(None, title="ラベル")
    priority: Optional[str] = Field(None, title="優先度", example="High")
    status: Optional[str] = Field(None, title="ステータス", example="TODO")


class TaskUpdateResponse(BaseSchema):
    id: uuid.UUID = Field(..., title="タスクID")
    message: str = Field(..., title="メッセージ")
