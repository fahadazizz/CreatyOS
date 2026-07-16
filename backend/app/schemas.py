from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


class OrmModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


def _strip_nonempty(value: str) -> str:
    stripped = value.strip()
    if not stripped:
        raise ValueError("must not be empty")
    return stripped


class WorkspaceCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    slug: str = Field(min_length=3, max_length=80, pattern=r"^[a-z0-9][a-z0-9-]*[a-z0-9]$")

    _name = field_validator("name")(_strip_nonempty)


class WorkspaceRead(OrmModel):
    id: UUID
    name: str
    slug: str
    created_at: datetime
    updated_at: datetime


class UserCreate(BaseModel):
    email: str = Field(min_length=3, max_length=320)
    display_name: str = Field(min_length=1, max_length=200)

    @field_validator("email")
    @classmethod
    def validate_email(cls, value: str) -> str:
        normalized = value.strip().lower()
        if "@" not in normalized or normalized.startswith("@") or normalized.endswith("@"):
            raise ValueError("must be a valid email-like address")
        return normalized

    _display_name = field_validator("display_name")(_strip_nonempty)


class UserRead(OrmModel):
    id: UUID
    email: str
    display_name: str
    created_at: datetime
    updated_at: datetime


class ProjectCreate(BaseModel):
    workspace_id: UUID
    owner_user_id: UUID
    title: str = Field(min_length=1, max_length=240)
    logline: str | None = Field(default=None, max_length=4000)

    _title = field_validator("title")(_strip_nonempty)


class ProjectRead(OrmModel):
    id: UUID
    workspace_id: UUID
    owner_user_id: UUID
    title: str
    logline: str | None
    status: str
    created_at: datetime
    updated_at: datetime


class ProductionCreate(BaseModel):
    title: str = Field(min_length=1, max_length=240)
    format: str = Field(min_length=1, max_length=80)

    _title = field_validator("title")(_strip_nonempty)
    _format = field_validator("format")(_strip_nonempty)


class ProductionRead(OrmModel):
    id: UUID
    project_id: UUID
    title: str
    format: str
    status: str
    created_at: datetime
    updated_at: datetime


class PieceCreate(BaseModel):
    title: str = Field(min_length=1, max_length=240)
    runtime_target_seconds: int | None = Field(default=None, ge=1)

    _title = field_validator("title")(_strip_nonempty)


class PieceRead(OrmModel):
    id: UUID
    production_id: UUID
    title: str
    status: str
    runtime_target_seconds: int | None
    created_at: datetime
    updated_at: datetime


class DeliverableCreate(BaseModel):
    name: str = Field(min_length=1, max_length=240)
    platform: str = Field(min_length=1, max_length=120)
    delivery_format: str = Field(min_length=1, max_length=120)

    _name = field_validator("name")(_strip_nonempty)
    _platform = field_validator("platform")(_strip_nonempty)
    _delivery_format = field_validator("delivery_format")(_strip_nonempty)


class DeliverableRead(OrmModel):
    id: UUID
    piece_id: UUID
    name: str
    platform: str
    delivery_format: str
    status: str
    created_at: datetime
    updated_at: datetime


class AuditEventRead(OrmModel):
    id: UUID
    actor_user_id: UUID | None
    workspace_id: UUID | None
    project_id: UUID | None
    entity_type: str
    entity_id: UUID
    action: str
    payload: dict[str, Any]
    created_at: datetime
