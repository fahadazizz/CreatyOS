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
    creative_inputs: Mapped[list["CreativeInput"]] = relationship(back_populates="project")
    blackboard_entries: Mapped[list["BlackboardEntry"]] = relationship(back_populates="project")
    deliberation_records: Mapped[list["DeliberationRecord"]] = relationship(back_populates="project")
    specialist_proposals: Mapped[list["SpecialistProposal"]] = relationship(back_populates="project")
    human_checkpoints: Mapped[list["HumanCheckpoint"]] = relationship(back_populates="project")


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


class CreativeInput(Base):
    __tablename__ = "creative_inputs"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    production_id: Mapped[str | None] = mapped_column(
        ForeignKey("productions.id"), nullable=True, index=True
    )
    piece_id: Mapped[str | None] = mapped_column(ForeignKey("pieces.id"), nullable=True, index=True)
    submitted_by_user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    input_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(240), nullable=False)
    source_label: Mapped[str | None] = mapped_column(String(240), nullable=True)
    candidate_state: Mapped[str] = mapped_column(String(40), nullable=False, default="candidate")
    body_json: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)

    project: Mapped[Project] = relationship(back_populates="creative_inputs")


class BlackboardEntry(TimestampMixin, Base):
    __tablename__ = "blackboard_entries"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    author_user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    entry_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(240), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    confidence_level: Mapped[str] = mapped_column(String(40), nullable=False)
    severity: Mapped[str] = mapped_column(String(40), nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="open", index=True)
    payload_json: Mapped[str] = mapped_column(Text, nullable=False)
    target_artifact_id: Mapped[str | None] = mapped_column(
        ForeignKey("artifacts.id"), nullable=True, index=True
    )
    target_artifact_version_id: Mapped[str | None] = mapped_column(
        ForeignKey("artifact_versions.id"), nullable=True, index=True
    )
    target_decision_id: Mapped[str | None] = mapped_column(
        ForeignKey("decisions.id"), nullable=True, index=True
    )
    target_creative_input_id: Mapped[str | None] = mapped_column(
        ForeignKey("creative_inputs.id"), nullable=True, index=True
    )

    project: Mapped[Project] = relationship(back_populates="blackboard_entries")


class DeliberationRecord(TimestampMixin, Base):
    __tablename__ = "deliberation_records"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    created_by_user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    phase: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    question: Mapped[str] = mapped_column(Text, nullable=False)
    recommended_next_action: Mapped[str] = mapped_column(Text, nullable=False)
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="open", index=True)
    priority_inputs_json: Mapped[str] = mapped_column(Text, nullable=False)
    linked_entry_ids_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    result_json: Mapped[str] = mapped_column(Text, nullable=False, default="{}")

    project: Mapped[Project] = relationship(back_populates="deliberation_records")


class SpecialistProposal(TimestampMixin, Base):
    __tablename__ = "specialist_proposals"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    submitted_by_user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    blackboard_entry_id: Mapped[str] = mapped_column(
        ForeignKey("blackboard_entries.id"), nullable=False, unique=True, index=True
    )
    specialist_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    proposal_kind: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(240), nullable=False)
    problem_statement: Mapped[str] = mapped_column(Text, nullable=False)
    recommendation: Mapped[str] = mapped_column(Text, nullable=False)
    rationale: Mapped[str] = mapped_column(Text, nullable=False)
    expected_impact: Mapped[str] = mapped_column(Text, nullable=False)
    confidence_level: Mapped[str] = mapped_column(String(40), nullable=False)
    severity: Mapped[str] = mapped_column(String(40), nullable=False)
    evidence_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    risks_json: Mapped[str] = mapped_column(Text, nullable=False, default="[]")
    status: Mapped[str] = mapped_column(String(40), nullable=False, default="submitted", index=True)
    target_artifact_id: Mapped[str | None] = mapped_column(
        ForeignKey("artifacts.id"), nullable=True, index=True
    )
    target_artifact_version_id: Mapped[str | None] = mapped_column(
        ForeignKey("artifact_versions.id"), nullable=True, index=True
    )
    target_decision_id: Mapped[str | None] = mapped_column(
        ForeignKey("decisions.id"), nullable=True, index=True
    )
    target_creative_input_id: Mapped[str | None] = mapped_column(
        ForeignKey("creative_inputs.id"), nullable=True, index=True
    )

    project: Mapped[Project] = relationship(back_populates="specialist_proposals")


class HumanCheckpoint(TimestampMixin, Base):
    __tablename__ = "human_checkpoints"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=new_id)
    project_id: Mapped[str] = mapped_column(ForeignKey("projects.id"), nullable=False, index=True)
    requested_by_user_id: Mapped[str] = mapped_column(
        ForeignKey("users.id"), nullable=False, index=True
    )
    decided_by_user_id: Mapped[str | None] = mapped_column(
        ForeignKey("users.id"), nullable=True, index=True
    )
    checkpoint_type: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(240), nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    decision_status: Mapped[str] = mapped_column(String(40), nullable=False, default="pending", index=True)
    decision_rationale: Mapped[str | None] = mapped_column(Text, nullable=True)
    linked_blackboard_entry_id: Mapped[str | None] = mapped_column(
        ForeignKey("blackboard_entries.id"), nullable=True, index=True
    )
    linked_deliberation_record_id: Mapped[str | None] = mapped_column(
        ForeignKey("deliberation_records.id"), nullable=True, index=True
    )
    target_artifact_id: Mapped[str | None] = mapped_column(
        ForeignKey("artifacts.id"), nullable=True, index=True
    )
    target_artifact_version_id: Mapped[str | None] = mapped_column(
        ForeignKey("artifact_versions.id"), nullable=True, index=True
    )
    target_decision_id: Mapped[str | None] = mapped_column(
        ForeignKey("decisions.id"), nullable=True, index=True
    )
    target_creative_input_id: Mapped[str | None] = mapped_column(
        ForeignKey("creative_inputs.id"), nullable=True, index=True
    )

    project: Mapped[Project] = relationship(back_populates="human_checkpoints")
