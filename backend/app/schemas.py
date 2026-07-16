from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator, model_validator


class OrmModel(BaseModel):
    model_config = ConfigDict(from_attributes=True)


def _strip_nonempty(value: str) -> str:
    stripped = value.strip()
    if not stripped:
        raise ValueError("must not be empty")
    return stripped


def _require_payload_keys(
    payload: dict[str, Any], entry_type: str, required_keys: tuple[str, ...]
) -> None:
    missing = [
        key
        for key in required_keys
        if key not in payload or payload[key] is None or payload[key] == ""
    ]
    if missing:
        raise ValueError(
            f"{entry_type} payload requires: {', '.join(required_keys)}"
        )


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


ArtifactType = Literal[
    "creative_problem",
    "editorial_point_of_view",
    "audience_experience",
    "story_argument_model",
    "direction_bible",
    "visual_language",
    "sound_direction",
    "production_constraints",
    "risk_register",
]

ConfidenceLevel = Literal["low", "medium", "high"]
DecisionStatus = Literal["proposed", "accepted", "rejected", "superseded"]
CreativeInputType = Literal[
    "raw_brief",
    "script",
    "research_notes",
    "reference",
    "brand_constraints",
    "audience_notes",
    "deliverables",
    "liked_example",
    "disliked_example",
]
CandidateState = Literal["candidate"]


class ArtifactCreate(BaseModel):
    owner_user_id: UUID
    artifact_type: ArtifactType
    title: str = Field(min_length=1, max_length=240)
    production_id: UUID | None = None
    piece_id: UUID | None = None

    _title = field_validator("title")(_strip_nonempty)


class ArtifactRead(OrmModel):
    id: UUID
    project_id: UUID
    production_id: UUID | None
    piece_id: UUID | None
    owner_user_id: UUID
    artifact_type: str
    title: str
    status: str
    created_at: datetime
    updated_at: datetime


class ArtifactVersionCreate(BaseModel):
    schema_version: str = Field(min_length=1, max_length=40)
    author_user_id: UUID
    confidence_level: ConfidenceLevel
    body: dict[str, Any]
    linked_decisions: list[UUID] = Field(default_factory=list)
    linked_evidence: list[str] = Field(default_factory=list, max_length=100)
    open_questions: list[str] = Field(default_factory=list, max_length=100)
    parent_version_id: UUID | None = None

    _schema_version = field_validator("schema_version")(_strip_nonempty)

    @field_validator("body")
    @classmethod
    def validate_body(cls, value: dict[str, Any]) -> dict[str, Any]:
        if not value:
            raise ValueError("body must not be empty")
        return value

    @field_validator("linked_evidence", "open_questions")
    @classmethod
    def validate_string_list(cls, value: list[str]) -> list[str]:
        cleaned = []
        for item in value:
            stripped = item.strip()
            if not stripped:
                raise ValueError("list items must not be empty")
            cleaned.append(stripped)
        return cleaned


class ArtifactVersionRead(OrmModel):
    id: UUID
    artifact_id: UUID
    version_number: int
    schema_version: str
    author_user_id: UUID
    parent_version_id: UUID | None
    confidence_level: str
    body: dict[str, Any]
    linked_decisions: list[UUID]
    linked_evidence: list[str]
    open_questions: list[str]
    created_at: datetime


class DecisionCreate(BaseModel):
    owner_user_id: UUID
    title: str = Field(min_length=1, max_length=240)
    decision_text: str = Field(min_length=1, max_length=4000)
    alternatives_considered: list[str] = Field(min_length=1, max_length=25)
    selected_option: str = Field(min_length=1, max_length=500)
    rationale: str = Field(min_length=1, max_length=4000)
    evidence: list[str] = Field(default_factory=list, max_length=100)
    risks: list[str] = Field(default_factory=list, max_length=100)
    affected_scope: dict[str, Any]
    target_artifact_id: UUID | None = None
    target_artifact_version_id: UUID | None = None
    status: DecisionStatus = "proposed"

    _title = field_validator("title")(_strip_nonempty)
    _decision_text = field_validator("decision_text")(_strip_nonempty)
    _selected_option = field_validator("selected_option")(_strip_nonempty)
    _rationale = field_validator("rationale")(_strip_nonempty)

    @field_validator("alternatives_considered", "evidence", "risks")
    @classmethod
    def validate_string_items(cls, value: list[str]) -> list[str]:
        cleaned = []
        for item in value:
            stripped = item.strip()
            if not stripped:
                raise ValueError("list items must not be empty")
            cleaned.append(stripped)
        return cleaned

    @field_validator("affected_scope")
    @classmethod
    def validate_affected_scope(cls, value: dict[str, Any]) -> dict[str, Any]:
        if not value:
            raise ValueError("affected_scope must not be empty")
        return value


class DecisionRead(OrmModel):
    id: UUID
    project_id: UUID
    owner_user_id: UUID
    target_artifact_id: UUID | None
    target_artifact_version_id: UUID | None
    title: str
    decision_text: str
    alternatives_considered: list[str]
    selected_option: str
    rationale: str
    evidence: list[str]
    risks: list[str]
    affected_scope: dict[str, Any]
    status: str
    created_at: datetime
    updated_at: datetime


class DecisionStatusUpdate(BaseModel):
    status: DecisionStatus


class CreativeInputCreate(BaseModel):
    submitted_by_user_id: UUID
    input_type: CreativeInputType
    title: str = Field(min_length=1, max_length=240)
    body: dict[str, Any]
    source_label: str | None = Field(default=None, max_length=240)
    production_id: UUID | None = None
    piece_id: UUID | None = None

    _title = field_validator("title")(_strip_nonempty)

    @field_validator("body")
    @classmethod
    def validate_body(cls, value: dict[str, Any]) -> dict[str, Any]:
        if not value:
            raise ValueError("body must not be empty")
        return value

    @field_validator("source_label")
    @classmethod
    def validate_source_label(cls, value: str | None) -> str | None:
        if value is None:
            return value
        return _strip_nonempty(value)


class CreativeInputRead(OrmModel):
    id: UUID
    project_id: UUID
    production_id: UUID | None
    piece_id: UUID | None
    submitted_by_user_id: UUID
    input_type: str
    title: str
    source_label: str | None
    candidate_state: CandidateState
    body: dict[str, Any]
    created_at: datetime


BlackboardEntryType = Literal[
    "observation",
    "proposal",
    "contradiction",
    "missing_information",
    "risk",
    "issue",
    "proof_request",
    "task_recommendation",
]
BlackboardEntryStatus = Literal["open", "accepted", "rejected", "resolved", "superseded"]
BlackboardSeverity = Literal["low", "medium", "high", "critical"]
DeliberationPhase = Literal[
    "sense",
    "frame",
    "diverge",
    "externalize",
    "experience",
    "critique",
    "decide",
    "commit",
    "propagate",
    "reopen",
]
DeliberationStatus = Literal["open", "recorded", "superseded"]
SpecialistType = Literal[
    "creative_director",
    "story_argument",
    "editorial",
    "visual_direction",
    "sound_direction",
    "producer",
    "critic",
]
SpecialistProposalKind = Literal[
    "creative_route",
    "story_argument",
    "editorial_action",
    "visual_direction",
    "sound_direction",
    "production_action",
    "critique",
    "proof_request",
    "risk_response",
]
SpecialistProposalStatus = Literal["submitted"]
HumanCheckpointType = Literal[
    "project_thesis",
    "creative_route",
    "audience_promise",
    "final_treatment",
    "visual_language",
    "production_plan",
    "edit_direction",
    "final_release",
]
HumanCheckpointStatus = Literal["pending", "approved", "revision_requested", "blocked"]
ScoreBranchStatus = Literal["draft", "active", "superseded"]
ScoreHierarchyLevel = Literal[
    "piece",
    "act",
    "sequence",
    "scene",
    "beat",
    "shot",
    "event",
    "cut",
]
ScoreEventStatus = Literal["planned", "needs_proof", "approved", "superseded"]
ScoreDurationPolicy = Literal["elastic", "fixed", "relative"]


BLACKBOARD_PAYLOAD_REQUIREMENTS: dict[BlackboardEntryType, tuple[str, ...]] = {
    "observation": ("observation", "evidence"),
    "proposal": ("proposal_type", "recommended_action", "expected_impact"),
    "contradiction": ("contradiction", "conflicts_with"),
    "missing_information": ("question", "needed_for"),
    "risk": ("risk_type", "impact", "mitigation"),
    "issue": ("issue_type", "impact", "mitigation"),
    "proof_request": (
        "proof_type",
        "question",
        "acceptance_test",
        "cheapest_useful_proof",
    ),
    "task_recommendation": (
        "task_type",
        "recommended_owner",
        "acceptance_criteria",
    ),
}


class BlackboardEntryCreate(BaseModel):
    author_user_id: UUID
    entry_type: BlackboardEntryType
    title: str = Field(min_length=1, max_length=240)
    summary: str = Field(min_length=1, max_length=4000)
    rationale: str = Field(min_length=1, max_length=4000)
    confidence_level: ConfidenceLevel
    severity: BlackboardSeverity
    payload: dict[str, Any]
    target_artifact_id: UUID | None = None
    target_artifact_version_id: UUID | None = None
    target_decision_id: UUID | None = None
    target_creative_input_id: UUID | None = None

    _title = field_validator("title")(_strip_nonempty)
    _summary = field_validator("summary")(_strip_nonempty)
    _rationale = field_validator("rationale")(_strip_nonempty)

    @model_validator(mode="after")
    def validate_structured_payload(self) -> "BlackboardEntryCreate":
        if not self.payload:
            raise ValueError("payload must not be empty")
        _require_payload_keys(
            self.payload,
            self.entry_type,
            BLACKBOARD_PAYLOAD_REQUIREMENTS[self.entry_type],
        )
        return self


class BlackboardEntryRead(OrmModel):
    id: UUID
    project_id: UUID
    author_user_id: UUID
    entry_type: str
    title: str
    summary: str
    rationale: str
    confidence_level: str
    severity: str
    status: str
    payload: dict[str, Any]
    target_artifact_id: UUID | None
    target_artifact_version_id: UUID | None
    target_decision_id: UUID | None
    target_creative_input_id: UUID | None
    created_at: datetime
    updated_at: datetime


class BlackboardEntryStatusUpdate(BaseModel):
    status: BlackboardEntryStatus


class DeliberationPriorityInputs(BaseModel):
    creative_impact: int = Field(ge=1, le=5)
    uncertainty: int = Field(ge=1, le=5)
    irreversibility: int = Field(ge=1, le=5)
    cost_of_delay: int = Field(ge=1, le=5)
    proof_cost: int = Field(ge=1, le=5)
    dependency_blockage: int = Field(ge=1, le=5)


class DeliberationRecordCreate(BaseModel):
    created_by_user_id: UUID
    phase: DeliberationPhase
    question: str = Field(min_length=1, max_length=4000)
    priority_inputs: DeliberationPriorityInputs
    linked_entry_ids: list[UUID] = Field(default_factory=list, max_length=100)
    recommended_next_action: str = Field(min_length=1, max_length=4000)
    rationale: str = Field(min_length=1, max_length=4000)
    result: dict[str, Any] = Field(default_factory=dict)

    _question = field_validator("question")(_strip_nonempty)
    _recommended_next_action = field_validator("recommended_next_action")(_strip_nonempty)
    _rationale = field_validator("rationale")(_strip_nonempty)

    @field_validator("linked_entry_ids")
    @classmethod
    def validate_linked_entry_ids(cls, value: list[UUID]) -> list[UUID]:
        if len(set(value)) != len(value):
            raise ValueError("linked_entry_ids must not contain duplicates")
        return value


class DeliberationRecordRead(OrmModel):
    id: UUID
    project_id: UUID
    created_by_user_id: UUID
    phase: str
    question: str
    priority_inputs: DeliberationPriorityInputs
    linked_entry_ids: list[UUID]
    recommended_next_action: str
    rationale: str
    result: dict[str, Any]
    status: str
    created_at: datetime
    updated_at: datetime


class DeliberationControllerRunCreate(BaseModel):
    created_by_user_id: UUID
    question: str = Field(default="What is the next most useful creative action?", max_length=4000)

    _question = field_validator("question")(_strip_nonempty)


class DeliberationCandidateRead(BaseModel):
    blackboard_entry_id: UUID
    entry_type: str
    title: str
    recommended_action: str
    priority_inputs: DeliberationPriorityInputs
    priority_score: float
    scoring_policy_version: str


class DeliberationControllerRunRead(BaseModel):
    deliberation_record: DeliberationRecordRead
    scoring_policy_version: str
    selected_candidate: DeliberationCandidateRead
    ranked_candidates: list[DeliberationCandidateRead]


class SpecialistProposalCreate(BaseModel):
    submitted_by_user_id: UUID
    specialist_type: SpecialistType
    proposal_kind: SpecialistProposalKind
    title: str = Field(min_length=1, max_length=240)
    problem_statement: str = Field(min_length=1, max_length=4000)
    recommendation: str = Field(min_length=1, max_length=4000)
    rationale: str = Field(min_length=1, max_length=4000)
    expected_impact: str = Field(min_length=1, max_length=4000)
    confidence_level: ConfidenceLevel
    severity: BlackboardSeverity
    evidence: list[str] = Field(default_factory=list, max_length=100)
    risks: list[str] = Field(default_factory=list, max_length=100)
    target_artifact_id: UUID | None = None
    target_artifact_version_id: UUID | None = None
    target_decision_id: UUID | None = None
    target_creative_input_id: UUID | None = None

    _title = field_validator("title")(_strip_nonempty)
    _problem_statement = field_validator("problem_statement")(_strip_nonempty)
    _recommendation = field_validator("recommendation")(_strip_nonempty)
    _rationale = field_validator("rationale")(_strip_nonempty)
    _expected_impact = field_validator("expected_impact")(_strip_nonempty)

    @field_validator("evidence", "risks")
    @classmethod
    def validate_string_items(cls, value: list[str]) -> list[str]:
        cleaned = []
        for item in value:
            stripped = item.strip()
            if not stripped:
                raise ValueError("list items must not be empty")
            cleaned.append(stripped)
        return cleaned


class SpecialistProposalRead(OrmModel):
    id: UUID
    project_id: UUID
    submitted_by_user_id: UUID
    blackboard_entry_id: UUID
    specialist_type: str
    proposal_kind: str
    title: str
    problem_statement: str
    recommendation: str
    rationale: str
    expected_impact: str
    confidence_level: str
    severity: str
    evidence: list[str]
    risks: list[str]
    status: str
    target_artifact_id: UUID | None
    target_artifact_version_id: UUID | None
    target_decision_id: UUID | None
    target_creative_input_id: UUID | None
    created_at: datetime
    updated_at: datetime


class HumanCheckpointCreate(BaseModel):
    requested_by_user_id: UUID
    checkpoint_type: HumanCheckpointType
    title: str = Field(min_length=1, max_length=240)
    summary: str = Field(min_length=1, max_length=4000)
    linked_blackboard_entry_id: UUID | None = None
    linked_deliberation_record_id: UUID | None = None
    target_artifact_id: UUID | None = None
    target_artifact_version_id: UUID | None = None
    target_decision_id: UUID | None = None
    target_creative_input_id: UUID | None = None

    _title = field_validator("title")(_strip_nonempty)
    _summary = field_validator("summary")(_strip_nonempty)


class HumanCheckpointDecisionUpdate(BaseModel):
    decided_by_user_id: UUID
    decision_status: Literal["approved", "revision_requested", "blocked"]
    decision_rationale: str = Field(min_length=1, max_length=4000)

    _decision_rationale = field_validator("decision_rationale")(_strip_nonempty)


class HumanCheckpointRead(OrmModel):
    id: UUID
    project_id: UUID
    requested_by_user_id: UUID
    decided_by_user_id: UUID | None
    checkpoint_type: str
    title: str
    summary: str
    decision_status: str
    decision_rationale: str | None
    linked_blackboard_entry_id: UUID | None
    linked_deliberation_record_id: UUID | None
    target_artifact_id: UUID | None
    target_artifact_version_id: UUID | None
    target_decision_id: UUID | None
    target_creative_input_id: UUID | None
    created_at: datetime
    updated_at: datetime


class HumanCheckpointReadinessItem(BaseModel):
    checkpoint_type: HumanCheckpointType
    status: HumanCheckpointStatus | Literal["missing"]
    checkpoint_id: UUID | None = None


class HumanCheckpointReadinessRead(BaseModel):
    project_id: UUID
    ready: bool
    required_checkpoint_types: list[HumanCheckpointType]
    approved_checkpoint_types: list[HumanCheckpointType]
    missing_checkpoint_types: list[HumanCheckpointType]
    blocked_checkpoint_types: list[HumanCheckpointType]
    revision_requested_checkpoint_types: list[HumanCheckpointType]
    items: list[HumanCheckpointReadinessItem]


class ScoreWhereWhen(BaseModel):
    placement: str = Field(min_length=1, max_length=1000)
    timing: str = Field(min_length=1, max_length=1000)
    duration: str = Field(min_length=1, max_length=1000)
    dependency: str = Field(min_length=1, max_length=1000)

    _placement = field_validator("placement")(_strip_nonempty)
    _timing = field_validator("timing")(_strip_nonempty)
    _duration = field_validator("duration")(_strip_nonempty)
    _dependency = field_validator("dependency")(_strip_nonempty)


class AudiovisualScoreBranchCreate(BaseModel):
    created_by_user_id: UUID
    name: str = Field(min_length=1, max_length=240)
    purpose: str = Field(min_length=1, max_length=4000)
    source_artifact_version_id: UUID | None = None
    source_decision_id: UUID | None = None

    _name = field_validator("name")(_strip_nonempty)
    _purpose = field_validator("purpose")(_strip_nonempty)


class AudiovisualScoreBranchRead(OrmModel):
    id: UUID
    project_id: UUID
    created_by_user_id: UUID
    name: str
    purpose: str
    status: str
    source_artifact_version_id: UUID | None
    source_decision_id: UUID | None
    created_at: datetime
    updated_at: datetime


class AudiovisualScoreEventCreate(BaseModel):
    created_by_user_id: UUID
    hierarchy_level: ScoreHierarchyLevel
    title: str = Field(min_length=1, max_length=240)
    sort_key: str = Field(min_length=1, max_length=120)
    why: str = Field(min_length=1, max_length=4000)
    what: str = Field(min_length=1, max_length=4000)
    how: str = Field(min_length=1, max_length=4000)
    where_when: ScoreWhereWhen
    duration_policy: ScoreDurationPolicy
    status: ScoreEventStatus = "planned"
    parent_event_id: UUID | None = None
    linked_artifact_version_id: UUID | None = None
    linked_decision_id: UUID | None = None
    linked_blackboard_entry_id: UUID | None = None

    _title = field_validator("title")(_strip_nonempty)
    _sort_key = field_validator("sort_key")(_strip_nonempty)
    _why = field_validator("why")(_strip_nonempty)
    _what = field_validator("what")(_strip_nonempty)
    _how = field_validator("how")(_strip_nonempty)


class AudiovisualScoreEventRead(OrmModel):
    id: UUID
    branch_id: UUID
    project_id: UUID
    created_by_user_id: UUID
    parent_event_id: UUID | None
    hierarchy_level: str
    title: str
    sort_key: str
    why: str
    what: str
    how: str
    where_when: ScoreWhereWhen
    duration_policy: str
    status: str
    linked_artifact_version_id: UUID | None
    linked_decision_id: UUID | None
    linked_blackboard_entry_id: UUID | None
    created_at: datetime
    updated_at: datetime
