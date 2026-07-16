from datetime import UTC, datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db import Base


def new_id() -> str:
    return str(uuid4())


def utcnow() -> datetime:
    return datetime.now(UTC)


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=utcnow, onupdate=utcnow
    )


class Workspace(TimestampMixin, Base):
    __tablename__ = "workspaces"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    slug: Mapped[str] = mapped_column(String(80), nullable=False, unique=True, index=True)

    projects: Mapped[list["Project"]] = relationship(back_populates="workspace")


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    email: Mapped[str] = mapped_column(String(320), nullable=False, unique=True, index=True)
    display_name: Mapped[str] = mapped_column(String(200), nullable=False)

    owned_projects: Mapped[list["Project"]] = relationship(back_populates="owner")


class Project(TimestampMixin, Base):
    __tablename__ = "projects"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    workspace_id: Mapped[str] = mapped_column(ForeignKey("workspaces.id"), nullable=False, index=True)
    owner_user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(240), nullable=False)
    logline: Mapped[str | None] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="active")

    workspace: Mapped[Workspace] = relationship(back_populates="projects")
    owner: Mapped[User] = relationship(back_populates="owned_projects")
    productions: Mapped[list["Production"]] = relationship(back_populates="project")
    artifacts: Mapped[list["Artifact"]] = relationship(back_populates="project")
    decisions: Mapped[list["Decision"]] = relationship(back_populates="project")


class Production(TimestampMixin, Base):
    __tablename__ = "productions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(240), nullable=False)
    format: Mapped[str] = mapped_column(String(80), nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="development")

    project: Mapped[Project] = relationship(back_populates="productions")
    pieces: Mapped[list["Piece"]] = relationship(back_populates="production")


class Piece(TimestampMixin, Base):
    __tablename__ = "pieces"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    production_id: Mapped[str] = mapped_column(ForeignKey("productions.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(240), nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="draft")
    runtime_target_seconds: Mapped[int | None] = mapped_column(Integer)

    production: Mapped[Production] = relationship(back_populates="pieces")
    deliverables: Mapped[list["Deliverable"]] = relationship(back_populates="piece")


class Deliverable(TimestampMixin, Base):
    __tablename__ = "deliverables"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    piece_id: Mapped[str] = mapped_column(ForeignKey("pieces.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(240), nullable=False)
    platform: Mapped[str] = mapped_column(String(120), nullable=False)
    delivery_format: Mapped[str] = mapped_column(String(120), nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="planned")

    piece: Mapped[Piece] = relationship(back_populates="deliverables")


class AuditEvent(Base):
    __tablename__ = "audit_events"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    actor_user_id: Mapped[str | None] = mapped_column(ForeignKey("users.id"), nullable=True, index=True)
    workspace_id: Mapped[str | None] = mapped_column(
        ForeignKey("workspaces.id"), nullable=True, index=True
    )
    project_id: Mapped[str | None] = mapped_column(ForeignKey("projects.id"), nullable=True, index=True)
    entity_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    entity_id: Mapped[str] = mapped_column(String(36), nullable=False, index=True)
    action: Mapped[str] = mapped_column(String(80), nullable=False)
    payload_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Artifact(TimestampMixin, Base):
    __tablename__ = "artifacts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    production_id: Mapped[str | None] = mapped_column(
        ForeignKey("productions.id"), nullable=True, index=True
    )
    piece_id: Mapped[str | None] = mapped_column(ForeignKey("pieces.id"), nullable=True, index=True)
    owner_user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    artifact_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(240), nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="draft")

    project: Mapped[Project] = relationship(back_populates="artifacts")
    versions: Mapped[list["ArtifactVersion"]] = relationship(
        back_populates="artifact", order_by="ArtifactVersion.version_number"
    )


class ArtifactVersion(Base):
    __tablename__ = "artifact_versions"
    __table_args__ = (
        UniqueConstraint("artifact_id", "version_number", name="uq_artifact_versions_number"),
    )

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    artifact_id: Mapped[str] = mapped_column(ForeignKey("artifacts.id"), nullable=False, index=True)
    version_number: Mapped[int] = mapped_column(Integer, nullable=False)
    schema_version: Mapped[str] = mapped_column(String(40), nullable=False)
    author_user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    parent_version_id: Mapped[str | None] = mapped_column(
        ForeignKey("artifact_versions.id"), nullable=True, index=True
    )
    confidence_level: Mapped[str] = mapped_column(String(40), nullable=False)
    body_json: Mapped[str] = mapped_column(Text, nullable=False)
    linked_decisions_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    linked_evidence_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    open_questions_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    artifact: Mapped[Artifact] = relationship(back_populates="versions")


class Decision(TimestampMixin, Base):
    __tablename__ = "decisions"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    owner_user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    target_artifact_id: Mapped[str | None] = mapped_column(
        ForeignKey("artifacts.id"), nullable=True, index=True
    )
    target_artifact_version_id: Mapped[str | None] = mapped_column(
        ForeignKey("artifact_versions.id"), nullable=True, index=True
    )
    title: Mapped[str] = mapped_column(String(240), nullable=False)
    decision_text: Mapped[str] = mapped_column(Text, nullable=False)
    selected_option: Mapped[str] = mapped_column(String(500), nullable=False)
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="proposed")
    alternatives_json: Mapped[str] = mapped_column(Text, nullable=False)
    evidence_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    risks_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    affected_scope_json: Mapped[str] = mapped_column(Text, nullable=False)

    project: Mapped[Project] = relationship(back_populates="decisions")
