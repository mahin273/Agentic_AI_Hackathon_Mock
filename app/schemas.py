from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, field_validator

from .models import Priority


class UserCreate(BaseModel):
    username: str
    password: str

    @field_validator("username", "password")
    @classmethod
    def validate_user_fields(cls, v, info):
        if not v or not v.strip():
            raise ValueError(f"{info.field_name} cannot be empty or whitespace only")
        if info.field_name == "password" and len(v) < 6:
            raise ValueError("password must be at least 6 characters long")
        return v.strip().lower() if info.field_name == "username" else v


class UserOut(BaseModel):
    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    priority: Priority = Priority.medium


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[datetime] = None
    priority: Optional[Priority] = None

    @field_validator("title", "priority")
    @classmethod
    def cannot_be_none(cls, v, info):
        if v is None:
            raise ValueError(f"{info.field_name} cannot be null")
        return v


class TodoOut(TodoBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
