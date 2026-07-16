import json
from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.artifact_contracts import validate_artifact_body
from app import models, schemas


class NotFoundError(Exception):
    def __init__(self, resource: str, resource_id: str) -> None:
        self.resource = resource
        self.resource_id = resource_id
        super().__init__(f"{resource} not found: {resource_id}")


class ConflictError(Exception):
    pass


class ValidationError(Exception):
    pass


def _one(db: Session, model: type, resource_id: str):
    item = db.get(model, resource_id)
    if item is None:
        raise NotFoundError(model.__name__, resource_id)
    return item


def _audit(
    db: Session,
    *,
    entity_type: str,
    entity_id: str,
    action: str,
    actor_user_id: str | None = None,
    workspace_id: str | None = None,
    project_id: str | None = None,
    payload: dict[str, Any] | None = None,
) -> models.AuditEvent:
    event = models.AuditEvent(
        actor_user_id=actor_user_id,
        workspace_id=workspace_id,
        project_id=project_id,
        entity_type=entity_type,
        entity_id=entity_id,
        action=action,
        payload_json=json.dumps(payload or {}, sort_keys=True),
    )
    db.add(event)
    return event


def _artifact_version_read(version: models.ArtifactVersion) -> schemas.ArtifactVersionRead:
    return schemas.ArtifactVersionRead.model_validate(
        {
            "id": version.id,
            "artifact_id": version.artifact_id,
            "version_number": version.version_number,
            "schema_version": version.schema_version,
            "author_user_id": version.author_user_id,
            "parent_version_id": version.parent_version_id,
            "confidence_level": version.confidence_level,
            "body": json.loads(version.body_json),
            "linked_decisions": json.loads(version.linked_decisions_json),
            "linked_evidence": json.loads(version.linked_evidence_json),
            "open_questions": json.loads(version.open_questions_json),
            "created_at": version.created_at,
        }
    )


def _decision_read(decision: models.Decision) -> schemas.DecisionRead:
    return schemas.DecisionRead.model_validate(
        {
            "id": decision.id,
            "project_id": decision.project_id,
            "owner_user_id": decision.owner_user_id,
            "target_artifact_id": decision.target_artifact_id,
            "target_artifact_version_id": decision.target_artifact_version_id,
            "title": decision.title,
            "decision_text": decision.decision_text,
            "alternatives_considered": json.loads(decision.alternatives_json),
            "selected_option": decision.selected_option,
            "rationale": decision.rationale,
            "evidence": json.loads(decision.evidence_json),
            "risks": json.loads(decision.risks_json),
            "affected_scope": json.loads(decision.affected_scope_json),
            "status": decision.status,
            "created_at": decision.created_at,
            "updated_at": decision.updated_at,
        }
    )


def _creative_input_read(creative_input: models.CreativeInput) -> schemas.CreativeInputRead:
    return schemas.CreativeInputRead.model_validate(
        {
            "id": creative_input.id,
            "project_id": creative_input.project_id,
            "production_id": creative_input.production_id,
            "piece_id": creative_input.piece_id,
            "submitted_by_user_id": creative_input.submitted_by_user_id,
            "input_type": creative_input.input_type,
            "title": creative_input.title,
            "source_label": creative_input.source_label,
            "candidate_state": creative_input.candidate_state,
            "body": json.loads(creative_input.body_json),
            "created_at": creative_input.created_at,
        }
    )


def _blackboard_entry_read(entry: models.BlackboardEntry) -> schemas.BlackboardEntryRead:
    return schemas.BlackboardEntryRead.model_validate(
        {
            "id": entry.id,
            "project_id": entry.project_id,
            "author_user_id": entry.author_user_id,
            "entry_type": entry.entry_type,
            "title": entry.title,
            "summary": entry.summary,
            "rationale": entry.rationale,
            "confidence_level": entry.confidence_level,
            "severity": entry.severity,
            "status": entry.status,
            "payload": json.loads(entry.payload_json),
            "target_artifact_id": entry.target_artifact_id,
            "target_artifact_version_id": entry.target_artifact_version_id,
            "target_decision_id": entry.target_decision_id,
            "target_creative_input_id": entry.target_creative_input_id,
            "created_at": entry.created_at,
            "updated_at": entry.updated_at,
        }
    )


def _deliberation_record_read(
    record: models.DeliberationRecord,
) -> schemas.DeliberationRecordRead:
    return schemas.DeliberationRecordRead.model_validate(
        {
            "id": record.id,
            "project_id": record.project_id,
            "created_by_user_id": record.created_by_user_id,
            "phase": record.phase,
            "question": record.question,
            "priority_inputs": json.loads(record.priority_inputs_json),
            "linked_entry_ids": json.loads(record.linked_entry_ids_json),
            "recommended_next_action": record.recommended_next_action,
            "rationale": record.rationale,
            "result": json.loads(record.result_json),
            "status": record.status,
            "created_at": record.created_at,
            "updated_at": record.updated_at,
        }
    )


def _specialist_proposal_read(
    proposal: models.SpecialistProposal,
) -> schemas.SpecialistProposalRead:
    return schemas.SpecialistProposalRead.model_validate(
        {
            "id": proposal.id,
            "project_id": proposal.project_id,
            "submitted_by_user_id": proposal.submitted_by_user_id,
            "blackboard_entry_id": proposal.blackboard_entry_id,
            "specialist_type": proposal.specialist_type,
            "proposal_kind": proposal.proposal_kind,
            "title": proposal.title,
            "problem_statement": proposal.problem_statement,
            "recommendation": proposal.recommendation,
            "rationale": proposal.rationale,
            "expected_impact": proposal.expected_impact,
            "confidence_level": proposal.confidence_level,
            "severity": proposal.severity,
            "evidence": json.loads(proposal.evidence_json),
            "risks": json.loads(proposal.risks_json),
            "status": proposal.status,
            "target_artifact_id": proposal.target_artifact_id,
            "target_artifact_version_id": proposal.target_artifact_version_id,
            "target_decision_id": proposal.target_decision_id,
            "target_creative_input_id": proposal.target_creative_input_id,
            "created_at": proposal.created_at,
            "updated_at": proposal.updated_at,
        }
    )


def _human_checkpoint_read(
    checkpoint: models.HumanCheckpoint,
) -> schemas.HumanCheckpointRead:
    return schemas.HumanCheckpointRead.model_validate(
        {
            "id": checkpoint.id,
            "project_id": checkpoint.project_id,
            "requested_by_user_id": checkpoint.requested_by_user_id,
            "decided_by_user_id": checkpoint.decided_by_user_id,
            "checkpoint_type": checkpoint.checkpoint_type,
            "title": checkpoint.title,
            "summary": checkpoint.summary,
            "decision_status": checkpoint.decision_status,
            "decision_rationale": checkpoint.decision_rationale,
            "linked_blackboard_entry_id": checkpoint.linked_blackboard_entry_id,
            "linked_deliberation_record_id": checkpoint.linked_deliberation_record_id,
            "target_artifact_id": checkpoint.target_artifact_id,
            "target_artifact_version_id": checkpoint.target_artifact_version_id,
            "target_decision_id": checkpoint.target_decision_id,
            "target_creative_input_id": checkpoint.target_creative_input_id,
            "created_at": checkpoint.created_at,
            "updated_at": checkpoint.updated_at,
        }
    )


def _score_branch_read(
    branch: models.AudiovisualScoreBranch,
) -> schemas.AudiovisualScoreBranchRead:
    return schemas.AudiovisualScoreBranchRead.model_validate(
        {
            "id": branch.id,
            "project_id": branch.project_id,
            "created_by_user_id": branch.created_by_user_id,
            "name": branch.name,
            "purpose": branch.purpose,
            "status": branch.status,
            "source_artifact_version_id": branch.source_artifact_version_id,
            "source_decision_id": branch.source_decision_id,
            "created_at": branch.created_at,
            "updated_at": branch.updated_at,
        }
    )


def _score_event_read(
    event: models.AudiovisualScoreEvent,
) -> schemas.AudiovisualScoreEventRead:
    return schemas.AudiovisualScoreEventRead.model_validate(
        {
            "id": event.id,
            "branch_id": event.branch_id,
            "project_id": event.project_id,
            "created_by_user_id": event.created_by_user_id,
            "parent_event_id": event.parent_event_id,
            "hierarchy_level": event.hierarchy_level,
            "title": event.title,
            "sort_key": event.sort_key,
            "why": event.why,
            "what": event.what,
            "how": event.how,
            "where_when": json.loads(event.where_when_json),
            "duration_policy": event.duration_policy,
            "status": event.status,
            "linked_artifact_version_id": event.linked_artifact_version_id,
            "linked_decision_id": event.linked_decision_id,
            "linked_blackboard_entry_id": event.linked_blackboard_entry_id,
            "created_at": event.created_at,
            "updated_at": event.updated_at,
        }
    )


def _score_lane_entry_read(
    entry: models.AudiovisualScoreLaneEntry,
) -> schemas.AudiovisualScoreLaneEntryRead:
    return schemas.AudiovisualScoreLaneEntryRead.model_validate(
        {
            "id": entry.id,
            "branch_id": entry.branch_id,
            "score_event_id": entry.score_event_id,
            "project_id": entry.project_id,
            "created_by_user_id": entry.created_by_user_id,
            "lane_type": entry.lane_type,
            "title": entry.title,
            "intent": entry.intent,
            "content": json.loads(entry.content_json),
            "status": entry.status,
            "linked_artifact_version_id": entry.linked_artifact_version_id,
            "linked_decision_id": entry.linked_decision_id,
            "linked_blackboard_entry_id": entry.linked_blackboard_entry_id,
            "created_at": entry.created_at,
            "updated_at": entry.updated_at,
        }
    )


def _score_event_relationship_read(
    relationship: models.AudiovisualScoreEventRelationship,
) -> schemas.AudiovisualScoreEventRelationshipRead:
    return schemas.AudiovisualScoreEventRelationshipRead.model_validate(
        {
            "id": relationship.id,
            "branch_id": relationship.branch_id,
            "project_id": relationship.project_id,
            "created_by_user_id": relationship.created_by_user_id,
            "from_event_id": relationship.from_event_id,
            "to_event_id": relationship.to_event_id,
            "relationship_type": relationship.relationship_type,
            "title": relationship.title,
            "rationale": relationship.rationale,
            "expected_viewer_effect": relationship.expected_viewer_effect,
            "timing_logic": relationship.timing_logic,
            "continuity_impact": relationship.continuity_impact,
            "status": relationship.status,
            "linked_artifact_version_id": relationship.linked_artifact_version_id,
            "linked_decision_id": relationship.linked_decision_id,
            "linked_blackboard_entry_id": relationship.linked_blackboard_entry_id,
            "created_at": relationship.created_at,
            "updated_at": relationship.updated_at,
        }
    )


def _score_preview_prototype_read(
    prototype: models.AudiovisualScorePreviewPrototype,
) -> schemas.AudiovisualScorePreviewPrototypeRead:
    return schemas.AudiovisualScorePreviewPrototypeRead.model_validate(
        {
            "id": prototype.id,
            "branch_id": prototype.branch_id,
            "project_id": prototype.project_id,
            "created_by_user_id": prototype.created_by_user_id,
            "prototype_type": prototype.prototype_type,
            "title": prototype.title,
            "purpose": prototype.purpose,
            "test_question": prototype.test_question,
            "status": prototype.status,
            "linked_decision_id": prototype.linked_decision_id,
            "linked_blackboard_entry_id": prototype.linked_blackboard_entry_id,
            "created_at": prototype.created_at,
            "updated_at": prototype.updated_at,
        }
    )


def _score_preview_item_read(
    item: models.AudiovisualScorePreviewItem,
) -> schemas.AudiovisualScorePreviewItemRead:
    return schemas.AudiovisualScorePreviewItemRead.model_validate(
        {
            "id": item.id,
            "prototype_id": item.prototype_id,
            "branch_id": item.branch_id,
            "score_event_id": item.score_event_id,
            "project_id": item.project_id,
            "created_by_user_id": item.created_by_user_id,
            "item_type": item.item_type,
            "title": item.title,
            "sort_key": item.sort_key,
            "test_focus": item.test_focus,
            "inspection_notes": item.inspection_notes,
            "score_event_why_snapshot": item.score_event_why_snapshot,
            "body": json.loads(item.body_json),
            "status": item.status,
            "linked_artifact_version_id": item.linked_artifact_version_id,
            "linked_decision_id": item.linked_decision_id,
            "linked_blackboard_entry_id": item.linked_blackboard_entry_id,
            "created_at": item.created_at,
            "updated_at": item.updated_at,
        }
    )


def _validate_blackboard_targets(
    db: Session,
    *,
    project: models.Project,
    target_artifact_id: str | None,
    target_artifact_version_id: str | None,
    target_decision_id: str | None,
    target_creative_input_id: str | None,
) -> None:
    if target_artifact_id is not None:
        artifact = _one(db, models.Artifact, target_artifact_id)
        if artifact.project_id != project.id:
            raise ValidationError("target artifact does not belong to project")

    if target_artifact_version_id is not None:
        artifact_version = _one(db, models.ArtifactVersion, target_artifact_version_id)
        version_artifact = _one(db, models.Artifact, artifact_version.artifact_id)
        if version_artifact.project_id != project.id:
            raise ValidationError("target artifact version does not belong to project")
        if target_artifact_id is not None and artifact_version.artifact_id != target_artifact_id:
            raise ValidationError("target artifact version does not belong to target artifact")

    if target_decision_id is not None:
        decision = _one(db, models.Decision, target_decision_id)
        if decision.project_id != project.id:
            raise ValidationError("target decision does not belong to project")

    if target_creative_input_id is not None:
        creative_input = _one(db, models.CreativeInput, target_creative_input_id)
        if creative_input.project_id != project.id:
            raise ValidationError("target creative input does not belong to project")


def _validate_checkpoint_links(
    db: Session,
    *,
    project: models.Project,
    linked_blackboard_entry_id: str | None,
    linked_deliberation_record_id: str | None,
) -> None:
    if linked_blackboard_entry_id is not None:
        entry = _one(db, models.BlackboardEntry, linked_blackboard_entry_id)
        if entry.project_id != project.id:
            raise ValidationError("linked blackboard entry does not belong to project")

    if linked_deliberation_record_id is not None:
        record = _one(db, models.DeliberationRecord, linked_deliberation_record_id)
        if record.project_id != project.id:
            raise ValidationError("linked deliberation record does not belong to project")


def _validate_score_links(
    db: Session,
    *,
    project: models.Project,
    artifact_version_id: str | None = None,
    decision_id: str | None = None,
    blackboard_entry_id: str | None = None,
) -> None:
    if artifact_version_id is not None:
        version = _one(db, models.ArtifactVersion, artifact_version_id)
        artifact = _one(db, models.Artifact, version.artifact_id)
        if artifact.project_id != project.id:
            raise ValidationError("linked artifact version does not belong to project")
    if decision_id is not None:
        decision = _one(db, models.Decision, decision_id)
        if decision.project_id != project.id:
            raise ValidationError("linked decision does not belong to project")
    if blackboard_entry_id is not None:
        entry = _one(db, models.BlackboardEntry, blackboard_entry_id)
        if entry.project_id != project.id:
            raise ValidationError("linked blackboard entry does not belong to project")


def create_workspace(db: Session, data: schemas.WorkspaceCreate) -> models.Workspace:
    workspace = models.Workspace(name=data.name, slug=data.slug)
    db.add(workspace)
    try:
        db.flush()
    except IntegrityError as exc:
        raise ConflictError("workspace slug already exists") from exc
    _audit(
        db,
        entity_type="workspace",
        entity_id=workspace.id,
        action="created",
        workspace_id=workspace.id,
        payload={"name": workspace.name, "slug": workspace.slug},
    )
    db.commit()
    db.refresh(workspace)
    return workspace


def create_user(db: Session, data: schemas.UserCreate) -> models.User:
    user = models.User(email=data.email, display_name=data.display_name)
    db.add(user)
    try:
        db.flush()
    except IntegrityError as exc:
        raise ConflictError("user email already exists") from exc
    _audit(
        db,
        entity_type="user",
        entity_id=user.id,
        action="created",
        actor_user_id=user.id,
        payload={"email": user.email},
    )
    db.commit()
    db.refresh(user)
    return user


def create_project(db: Session, data: schemas.ProjectCreate) -> models.Project:
    _one(db, models.Workspace, str(data.workspace_id))
    _one(db, models.User, str(data.owner_user_id))
    project = models.Project(
        workspace_id=str(data.workspace_id),
        owner_user_id=str(data.owner_user_id),
        title=data.title,
        logline=data.logline,
    )
    db.add(project)
    db.flush()
    _audit(
        db,
        entity_type="project",
        entity_id=project.id,
        action="created",
        actor_user_id=project.owner_user_id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        payload={"title": project.title},
    )
    db.commit()
    db.refresh(project)
    return project


def list_projects(db: Session) -> list[models.Project]:
    return list(db.scalars(select(models.Project).order_by(models.Project.created_at)).all())


def get_project(db: Session, project_id: str) -> models.Project:
    return _one(db, models.Project, project_id)


def create_production(
    db: Session, project_id: str, data: schemas.ProductionCreate
) -> models.Production:
    project = _one(db, models.Project, project_id)
    production = models.Production(project_id=project.id, title=data.title, format=data.format)
    db.add(production)
    db.flush()
    _audit(
        db,
        entity_type="production",
        entity_id=production.id,
        action="created",
        actor_user_id=project.owner_user_id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        payload={"title": production.title, "format": production.format},
    )
    db.commit()
    db.refresh(production)
    return production


def create_piece(db: Session, production_id: str, data: schemas.PieceCreate) -> models.Piece:
    production = _one(db, models.Production, production_id)
    project = _one(db, models.Project, production.project_id)
    piece = models.Piece(
        production_id=production.id,
        title=data.title,
        runtime_target_seconds=data.runtime_target_seconds,
    )
    db.add(piece)
    db.flush()
    _audit(
        db,
        entity_type="piece",
        entity_id=piece.id,
        action="created",
        actor_user_id=project.owner_user_id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        payload={"title": piece.title},
    )
    db.commit()
    db.refresh(piece)
    return piece


def create_deliverable(
    db: Session, piece_id: str, data: schemas.DeliverableCreate
) -> models.Deliverable:
    piece = _one(db, models.Piece, piece_id)
    production = _one(db, models.Production, piece.production_id)
    project = _one(db, models.Project, production.project_id)
    deliverable = models.Deliverable(
        piece_id=piece.id,
        name=data.name,
        platform=data.platform,
        delivery_format=data.delivery_format,
    )
    db.add(deliverable)
    db.flush()
    _audit(
        db,
        entity_type="deliverable",
        entity_id=deliverable.id,
        action="created",
        actor_user_id=project.owner_user_id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        payload={
            "name": deliverable.name,
            "platform": deliverable.platform,
            "delivery_format": deliverable.delivery_format,
        },
    )
    db.commit()
    db.refresh(deliverable)
    return deliverable


def list_audit_events(db: Session, project_id: str | None = None) -> list[schemas.AuditEventRead]:
    query = select(models.AuditEvent).order_by(models.AuditEvent.created_at)
    if project_id is not None:
        query = query.where(models.AuditEvent.project_id == project_id)
    events = db.scalars(query).all()
    return [
        schemas.AuditEventRead.model_validate(
            {
                "id": event.id,
                "actor_user_id": event.actor_user_id,
                "workspace_id": event.workspace_id,
                "project_id": event.project_id,
                "entity_type": event.entity_type,
                "entity_id": event.entity_id,
                "action": event.action,
                "payload": json.loads(event.payload_json),
                "created_at": event.created_at,
            }
        )
        for event in events
    ]


def create_artifact(
    db: Session, project_id: str, data: schemas.ArtifactCreate
) -> models.Artifact:
    project = _one(db, models.Project, project_id)
    _one(db, models.User, str(data.owner_user_id))

    production_id = str(data.production_id) if data.production_id else None
    piece_id = str(data.piece_id) if data.piece_id else None

    if production_id is not None:
        production = _one(db, models.Production, production_id)
        if production.project_id != project.id:
            raise ValidationError("production does not belong to project")

    if piece_id is not None:
        piece = _one(db, models.Piece, piece_id)
        production = _one(db, models.Production, piece.production_id)
        if production.project_id != project.id:
            raise ValidationError("piece does not belong to project")
        if production_id is not None and piece.production_id != production_id:
            raise ValidationError("piece does not belong to production")

    artifact = models.Artifact(
        project_id=project.id,
        production_id=production_id,
        piece_id=piece_id,
        owner_user_id=str(data.owner_user_id),
        artifact_type=data.artifact_type,
        title=data.title,
    )
    db.add(artifact)
    db.flush()
    _audit(
        db,
        entity_type="artifact",
        entity_id=artifact.id,
        action="created",
        actor_user_id=artifact.owner_user_id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        payload={"artifact_type": artifact.artifact_type, "title": artifact.title},
    )
    db.commit()
    db.refresh(artifact)
    return artifact


def list_project_artifacts(db: Session, project_id: str) -> list[models.Artifact]:
    _one(db, models.Project, project_id)
    return list(
        db.scalars(
            select(models.Artifact)
            .where(models.Artifact.project_id == project_id)
            .order_by(models.Artifact.created_at)
        ).all()
    )


def get_artifact(db: Session, artifact_id: str) -> models.Artifact:
    return _one(db, models.Artifact, artifact_id)


def create_artifact_version(
    db: Session, artifact_id: str, data: schemas.ArtifactVersionCreate
) -> schemas.ArtifactVersionRead:
    artifact = _one(db, models.Artifact, artifact_id)
    project = _one(db, models.Project, artifact.project_id)
    _one(db, models.User, str(data.author_user_id))
    try:
        validated_body = validate_artifact_body(
            artifact_type=artifact.artifact_type,
            schema_version=data.schema_version,
            body=data.body,
        )
    except ValueError as exc:
        raise ValidationError(str(exc)) from exc

    parent_version_id = str(data.parent_version_id) if data.parent_version_id else None
    if parent_version_id is not None:
        parent = _one(db, models.ArtifactVersion, parent_version_id)
        if parent.artifact_id != artifact.id:
            raise ValidationError("parent version does not belong to artifact")

    for decision_id in data.linked_decisions:
        decision = _one(db, models.Decision, str(decision_id))
        if decision.project_id != project.id:
            raise ValidationError("linked decision does not belong to artifact project")

    latest_number = db.scalar(
        select(models.ArtifactVersion.version_number)
        .where(models.ArtifactVersion.artifact_id == artifact.id)
        .order_by(models.ArtifactVersion.version_number.desc())
        .limit(1)
    )
    version_number = (latest_number or 0) + 1

    version = models.ArtifactVersion(
        artifact_id=artifact.id,
        version_number=version_number,
        schema_version=data.schema_version,
        author_user_id=str(data.author_user_id),
        parent_version_id=parent_version_id,
        confidence_level=data.confidence_level,
        body_json=json.dumps(validated_body, sort_keys=True),
        linked_decisions_json=json.dumps([str(item) for item in data.linked_decisions]),
        linked_evidence_json=json.dumps(data.linked_evidence),
        open_questions_json=json.dumps(data.open_questions),
    )
    db.add(version)
    try:
        db.flush()
    except IntegrityError as exc:
        db.rollback()
        raise ConflictError("artifact version number conflict; retry version creation") from exc
    _audit(
        db,
        entity_type="artifact_version",
        entity_id=version.id,
        action="created",
        actor_user_id=version.author_user_id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        payload={
            "artifact_id": artifact.id,
            "artifact_type": artifact.artifact_type,
            "version_number": version.version_number,
            "schema_version": version.schema_version,
        },
    )
    db.commit()
    db.refresh(version)
    return _artifact_version_read(version)


def list_artifact_versions(db: Session, artifact_id: str) -> list[schemas.ArtifactVersionRead]:
    _one(db, models.Artifact, artifact_id)
    versions = db.scalars(
        select(models.ArtifactVersion)
        .where(models.ArtifactVersion.artifact_id == artifact_id)
        .order_by(models.ArtifactVersion.version_number)
    ).all()
    return [_artifact_version_read(version) for version in versions]


def create_decision(
    db: Session, project_id: str, data: schemas.DecisionCreate
) -> schemas.DecisionRead:
    project = _one(db, models.Project, project_id)
    _one(db, models.User, str(data.owner_user_id))

    alternatives = data.alternatives_considered
    if data.selected_option not in alternatives:
        raise ValidationError("selected_option must be one of alternatives_considered")

    target_artifact_id = str(data.target_artifact_id) if data.target_artifact_id else None
    target_artifact_version_id = (
        str(data.target_artifact_version_id) if data.target_artifact_version_id else None
    )

    if target_artifact_id is not None:
        artifact = _one(db, models.Artifact, target_artifact_id)
        if artifact.project_id != project.id:
            raise ValidationError("target artifact does not belong to project")

    if target_artifact_version_id is not None:
        artifact_version = _one(db, models.ArtifactVersion, target_artifact_version_id)
        version_artifact = _one(db, models.Artifact, artifact_version.artifact_id)
        if version_artifact.project_id != project.id:
            raise ValidationError("target artifact version does not belong to project")
        if target_artifact_id is not None and artifact_version.artifact_id != target_artifact_id:
            raise ValidationError("target artifact version does not belong to target artifact")

    decision = models.Decision(
        project_id=project.id,
        owner_user_id=str(data.owner_user_id),
        target_artifact_id=target_artifact_id,
        target_artifact_version_id=target_artifact_version_id,
        title=data.title,
        decision_text=data.decision_text,
        selected_option=data.selected_option,
        rationale=data.rationale,
        status=data.status,
        alternatives_json=json.dumps(alternatives),
        evidence_json=json.dumps(data.evidence),
        risks_json=json.dumps(data.risks),
        affected_scope_json=json.dumps(data.affected_scope, sort_keys=True),
    )
    db.add(decision)
    db.flush()
    _audit(
        db,
        entity_type="decision",
        entity_id=decision.id,
        action="created",
        actor_user_id=decision.owner_user_id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        payload={
            "title": decision.title,
            "status": decision.status,
            "target_artifact_id": decision.target_artifact_id,
            "target_artifact_version_id": decision.target_artifact_version_id,
        },
    )
    db.commit()
    db.refresh(decision)
    return _decision_read(decision)


def list_project_decisions(db: Session, project_id: str) -> list[schemas.DecisionRead]:
    _one(db, models.Project, project_id)
    decisions = db.scalars(
        select(models.Decision)
        .where(models.Decision.project_id == project_id)
        .order_by(models.Decision.created_at)
    ).all()
    return [_decision_read(decision) for decision in decisions]


def get_decision(db: Session, decision_id: str) -> schemas.DecisionRead:
    return _decision_read(_one(db, models.Decision, decision_id))


def update_decision_status(
    db: Session, decision_id: str, data: schemas.DecisionStatusUpdate
) -> schemas.DecisionRead:
    decision = _one(db, models.Decision, decision_id)
    old_status = decision.status
    decision.status = data.status
    db.flush()
    project = _one(db, models.Project, decision.project_id)
    _audit(
        db,
        entity_type="decision",
        entity_id=decision.id,
        action="status_changed",
        actor_user_id=decision.owner_user_id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        payload={"old_status": old_status, "new_status": decision.status},
    )
    db.commit()
    db.refresh(decision)
    return _decision_read(decision)


def create_creative_input(
    db: Session, project_id: str, data: schemas.CreativeInputCreate
) -> schemas.CreativeInputRead:
    project = _one(db, models.Project, project_id)
    _one(db, models.User, str(data.submitted_by_user_id))

    production_id = str(data.production_id) if data.production_id else None
    piece_id = str(data.piece_id) if data.piece_id else None

    if production_id is not None:
        production = _one(db, models.Production, production_id)
        if production.project_id != project.id:
            raise ValidationError("production does not belong to project")

    if piece_id is not None:
        piece = _one(db, models.Piece, piece_id)
        production = _one(db, models.Production, piece.production_id)
        if production.project_id != project.id:
            raise ValidationError("piece does not belong to project")
        if production_id is not None and piece.production_id != production_id:
            raise ValidationError("piece does not belong to production")

    creative_input = models.CreativeInput(
        project_id=project.id,
        production_id=production_id,
        piece_id=piece_id,
        submitted_by_user_id=str(data.submitted_by_user_id),
        input_type=data.input_type,
        title=data.title,
        source_label=data.source_label,
        candidate_state="candidate",
        body_json=json.dumps(data.body, sort_keys=True),
    )
    db.add(creative_input)
    db.flush()
    _audit(
        db,
        entity_type="creative_input",
        entity_id=creative_input.id,
        action="created",
        actor_user_id=creative_input.submitted_by_user_id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        payload={
            "input_type": creative_input.input_type,
            "title": creative_input.title,
            "candidate_state": creative_input.candidate_state,
        },
    )
    db.commit()
    db.refresh(creative_input)
    return _creative_input_read(creative_input)


def list_project_creative_inputs(
    db: Session, project_id: str, input_type: str | None = None
) -> list[schemas.CreativeInputRead]:
    _one(db, models.Project, project_id)
    query = (
        select(models.CreativeInput)
        .where(models.CreativeInput.project_id == project_id)
        .order_by(models.CreativeInput.created_at)
    )
    if input_type is not None:
        query = query.where(models.CreativeInput.input_type == input_type)
    return [_creative_input_read(item) for item in db.scalars(query).all()]


def get_creative_input(db: Session, creative_input_id: str) -> schemas.CreativeInputRead:
    return _creative_input_read(_one(db, models.CreativeInput, creative_input_id))


def create_blackboard_entry(
    db: Session, project_id: str, data: schemas.BlackboardEntryCreate
) -> schemas.BlackboardEntryRead:
    project = _one(db, models.Project, project_id)
    _one(db, models.User, str(data.author_user_id))

    target_artifact_id = str(data.target_artifact_id) if data.target_artifact_id else None
    target_artifact_version_id = (
        str(data.target_artifact_version_id) if data.target_artifact_version_id else None
    )
    target_decision_id = str(data.target_decision_id) if data.target_decision_id else None
    target_creative_input_id = (
        str(data.target_creative_input_id) if data.target_creative_input_id else None
    )
    _validate_blackboard_targets(
        db,
        project=project,
        target_artifact_id=target_artifact_id,
        target_artifact_version_id=target_artifact_version_id,
        target_decision_id=target_decision_id,
        target_creative_input_id=target_creative_input_id,
    )

    entry = models.BlackboardEntry(
        project_id=project.id,
        author_user_id=str(data.author_user_id),
        entry_type=data.entry_type,
        title=data.title,
        summary=data.summary,
        rationale=data.rationale,
        confidence_level=data.confidence_level,
        severity=data.severity,
        status="open",
        payload_json=json.dumps(data.payload, sort_keys=True),
        target_artifact_id=target_artifact_id,
        target_artifact_version_id=target_artifact_version_id,
        target_decision_id=target_decision_id,
        target_creative_input_id=target_creative_input_id,
    )
    db.add(entry)
    db.flush()
    _audit(
        db,
        entity_type="blackboard_entry",
        entity_id=entry.id,
        action="created",
        actor_user_id=entry.author_user_id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        payload={
            "entry_type": entry.entry_type,
            "title": entry.title,
            "status": entry.status,
            "severity": entry.severity,
        },
    )
    db.commit()
    db.refresh(entry)
    return _blackboard_entry_read(entry)


def list_project_blackboard_entries(
    db: Session,
    project_id: str,
    entry_type: str | None = None,
    status: str | None = None,
) -> list[schemas.BlackboardEntryRead]:
    _one(db, models.Project, project_id)
    query = (
        select(models.BlackboardEntry)
        .where(models.BlackboardEntry.project_id == project_id)
        .order_by(models.BlackboardEntry.created_at)
    )
    if entry_type is not None:
        query = query.where(models.BlackboardEntry.entry_type == entry_type)
    if status is not None:
        query = query.where(models.BlackboardEntry.status == status)
    return [_blackboard_entry_read(entry) for entry in db.scalars(query).all()]


def get_blackboard_entry(db: Session, entry_id: str) -> schemas.BlackboardEntryRead:
    return _blackboard_entry_read(_one(db, models.BlackboardEntry, entry_id))


def update_blackboard_entry_status(
    db: Session, entry_id: str, data: schemas.BlackboardEntryStatusUpdate
) -> schemas.BlackboardEntryRead:
    entry = _one(db, models.BlackboardEntry, entry_id)
    old_status = entry.status
    entry.status = data.status
    db.flush()
    project = _one(db, models.Project, entry.project_id)
    _audit(
        db,
        entity_type="blackboard_entry",
        entity_id=entry.id,
        action="status_changed",
        actor_user_id=entry.author_user_id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        payload={"old_status": old_status, "new_status": entry.status},
    )
    db.commit()
    db.refresh(entry)
    return _blackboard_entry_read(entry)


_SEVERITY_SCORE = {"low": 1, "medium": 2, "high": 4, "critical": 5}
_CONFIDENCE_UNCERTAINTY = {"high": 1, "medium": 3, "low": 5}
_ENTRY_IMPACT = {
    "proof_request": 5,
    "risk": 5,
    "issue": 4,
    "contradiction": 4,
    "missing_information": 4,
    "proposal": 3,
    "task_recommendation": 3,
    "observation": 2,
}
_ENTRY_IRREVERSIBILITY = {
    "proof_request": 5,
    "risk": 5,
    "issue": 4,
    "contradiction": 4,
    "missing_information": 3,
    "proposal": 3,
    "task_recommendation": 2,
    "observation": 2,
}
_ENTRY_PROOF_COST = {
    "proof_request": 2,
    "risk": 3,
    "issue": 3,
    "contradiction": 3,
    "missing_information": 2,
    "proposal": 3,
    "task_recommendation": 3,
    "observation": 4,
}
DELIBERATION_SCORING_POLICY_VERSION = "deterministic_v1"
REQUIRED_HUMAN_CHECKPOINT_TYPES = [
    "project_thesis",
    "creative_route",
    "audience_promise",
    "final_treatment",
    "visual_language",
    "production_plan",
    "edit_direction",
    "final_release",
]


def _priority_inputs_for_entry(
    entry: models.BlackboardEntry,
) -> schemas.DeliberationPriorityInputs:
    payload = json.loads(entry.payload_json)
    dependency_blockage = 5 if entry.entry_type in {
        "proof_request",
        "risk",
        "issue",
        "missing_information",
    } else 3
    if payload.get("needed_for") or payload.get("acceptance_test"):
        dependency_blockage = 5

    return schemas.DeliberationPriorityInputs(
        creative_impact=_ENTRY_IMPACT[entry.entry_type],
        uncertainty=_CONFIDENCE_UNCERTAINTY[entry.confidence_level],
        irreversibility=_ENTRY_IRREVERSIBILITY[entry.entry_type],
        cost_of_delay=_SEVERITY_SCORE[entry.severity],
        proof_cost=_ENTRY_PROOF_COST[entry.entry_type],
        dependency_blockage=dependency_blockage,
    )


def _priority_score(priority_inputs: schemas.DeliberationPriorityInputs) -> float:
    numerator = (
        priority_inputs.creative_impact
        * priority_inputs.uncertainty
        * priority_inputs.irreversibility
        * priority_inputs.cost_of_delay
        * priority_inputs.dependency_blockage
    )
    return round(numerator / priority_inputs.proof_cost, 2)


def _recommended_action_for_entry(entry: models.BlackboardEntry) -> str:
    payload = json.loads(entry.payload_json)
    if entry.entry_type == "proof_request":
        return f"Request proof: {payload['cheapest_useful_proof']}"
    if entry.entry_type == "proposal":
        return payload["recommended_action"]
    if entry.entry_type == "risk":
        return f"Mitigate risk: {payload['mitigation']}"
    if entry.entry_type == "issue":
        return f"Resolve issue: {payload['mitigation']}"
    if entry.entry_type == "missing_information":
        return f"Answer missing information: {payload['question']}"
    if entry.entry_type == "contradiction":
        return f"Resolve contradiction: {payload['contradiction']}"
    if entry.entry_type == "task_recommendation":
        return payload["acceptance_criteria"]
    return f"Review observation: {payload['observation']}"


def _deliberation_candidate_read(
    entry: models.BlackboardEntry,
) -> schemas.DeliberationCandidateRead:
    priority_inputs = _priority_inputs_for_entry(entry)
    return schemas.DeliberationCandidateRead.model_validate(
        {
            "blackboard_entry_id": entry.id,
            "entry_type": entry.entry_type,
            "title": entry.title,
            "recommended_action": _recommended_action_for_entry(entry),
            "priority_inputs": priority_inputs,
            "priority_score": _priority_score(priority_inputs),
            "scoring_policy_version": DELIBERATION_SCORING_POLICY_VERSION,
        }
    )


def run_deliberation_controller(
    db: Session, project_id: str, data: schemas.DeliberationControllerRunCreate
) -> schemas.DeliberationControllerRunRead:
    project = _one(db, models.Project, project_id)
    _one(db, models.User, str(data.created_by_user_id))
    entries = db.scalars(
        select(models.BlackboardEntry)
        .where(models.BlackboardEntry.project_id == project.id)
        .where(models.BlackboardEntry.status == "open")
        .order_by(models.BlackboardEntry.created_at)
    ).all()
    if not entries:
        raise ValidationError("deliberation controller requires at least one open blackboard entry")

    ranked_candidates = sorted(
        [_deliberation_candidate_read(entry) for entry in entries],
        key=lambda candidate: (-candidate.priority_score, str(candidate.blackboard_entry_id)),
    )
    selected = ranked_candidates[0]
    record = models.DeliberationRecord(
        project_id=project.id,
        created_by_user_id=str(data.created_by_user_id),
        phase="decide",
        question=data.question,
        priority_inputs_json=json.dumps(selected.priority_inputs.model_dump(), sort_keys=True),
        linked_entry_ids_json=json.dumps([str(selected.blackboard_entry_id)]),
        recommended_next_action=selected.recommended_action,
        rationale=(
            "Deterministic priority heuristic selected the open entry with the highest "
            "impact, uncertainty, irreversibility, delay cost, and blockage relative to proof cost."
        ),
        result_json=json.dumps(
            {
                "controller": DELIBERATION_SCORING_POLICY_VERSION,
                "scoring_policy_version": DELIBERATION_SCORING_POLICY_VERSION,
                "selected_blackboard_entry_id": str(selected.blackboard_entry_id),
                "ranked_candidates": [
                    candidate.model_dump(mode="json") for candidate in ranked_candidates
                ],
            },
            sort_keys=True,
        ),
        status="recorded",
    )
    db.add(record)
    db.flush()
    _audit(
        db,
        entity_type="deliberation_record",
        entity_id=record.id,
        action="controller_ran",
        actor_user_id=record.created_by_user_id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        payload={
            "selected_blackboard_entry_id": str(selected.blackboard_entry_id),
            "selected_priority_score": selected.priority_score,
            "candidate_count": len(ranked_candidates),
        },
    )
    db.commit()
    db.refresh(record)
    return schemas.DeliberationControllerRunRead(
        deliberation_record=_deliberation_record_read(record),
        scoring_policy_version=DELIBERATION_SCORING_POLICY_VERSION,
        selected_candidate=selected,
        ranked_candidates=ranked_candidates,
    )


def create_deliberation_record(
    db: Session, project_id: str, data: schemas.DeliberationRecordCreate
) -> schemas.DeliberationRecordRead:
    project = _one(db, models.Project, project_id)
    _one(db, models.User, str(data.created_by_user_id))

    linked_entry_ids = [str(entry_id) for entry_id in data.linked_entry_ids]
    for entry_id in linked_entry_ids:
        entry = _one(db, models.BlackboardEntry, entry_id)
        if entry.project_id != project.id:
            raise ValidationError("linked blackboard entry does not belong to project")

    record = models.DeliberationRecord(
        project_id=project.id,
        created_by_user_id=str(data.created_by_user_id),
        phase=data.phase,
        question=data.question,
        priority_inputs_json=json.dumps(data.priority_inputs.model_dump(), sort_keys=True),
        linked_entry_ids_json=json.dumps(linked_entry_ids),
        recommended_next_action=data.recommended_next_action,
        rationale=data.rationale,
        result_json=json.dumps(data.result, sort_keys=True),
        status="open",
    )
    db.add(record)
    db.flush()
    _audit(
        db,
        entity_type="deliberation_record",
        entity_id=record.id,
        action="created",
        actor_user_id=record.created_by_user_id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        payload={
            "phase": record.phase,
            "status": record.status,
            "linked_entry_count": len(linked_entry_ids),
        },
    )
    db.commit()
    db.refresh(record)
    return _deliberation_record_read(record)


def list_project_deliberation_records(
    db: Session, project_id: str
) -> list[schemas.DeliberationRecordRead]:
    _one(db, models.Project, project_id)
    records = db.scalars(
        select(models.DeliberationRecord)
        .where(models.DeliberationRecord.project_id == project_id)
        .order_by(models.DeliberationRecord.created_at)
    ).all()
    return [_deliberation_record_read(record) for record in records]


def get_deliberation_record(
    db: Session, deliberation_id: str
) -> schemas.DeliberationRecordRead:
    return _deliberation_record_read(_one(db, models.DeliberationRecord, deliberation_id))


def create_specialist_proposal(
    db: Session, project_id: str, data: schemas.SpecialistProposalCreate
) -> schemas.SpecialistProposalRead:
    project = _one(db, models.Project, project_id)
    _one(db, models.User, str(data.submitted_by_user_id))

    target_artifact_id = str(data.target_artifact_id) if data.target_artifact_id else None
    target_artifact_version_id = (
        str(data.target_artifact_version_id) if data.target_artifact_version_id else None
    )
    target_decision_id = str(data.target_decision_id) if data.target_decision_id else None
    target_creative_input_id = (
        str(data.target_creative_input_id) if data.target_creative_input_id else None
    )
    _validate_blackboard_targets(
        db,
        project=project,
        target_artifact_id=target_artifact_id,
        target_artifact_version_id=target_artifact_version_id,
        target_decision_id=target_decision_id,
        target_creative_input_id=target_creative_input_id,
    )

    blackboard_payload = {
        "proposal_type": data.proposal_kind,
        "specialist_type": data.specialist_type,
        "problem_statement": data.problem_statement,
        "recommended_action": data.recommendation,
        "expected_impact": data.expected_impact,
        "evidence": data.evidence,
        "risks": data.risks,
    }
    entry = models.BlackboardEntry(
        project_id=project.id,
        author_user_id=str(data.submitted_by_user_id),
        entry_type="proposal",
        title=data.title,
        summary=data.problem_statement,
        rationale=data.rationale,
        confidence_level=data.confidence_level,
        severity=data.severity,
        status="open",
        payload_json=json.dumps(blackboard_payload, sort_keys=True),
        target_artifact_id=target_artifact_id,
        target_artifact_version_id=target_artifact_version_id,
        target_decision_id=target_decision_id,
        target_creative_input_id=target_creative_input_id,
    )
    db.add(entry)
    db.flush()

    proposal = models.SpecialistProposal(
        project_id=project.id,
        submitted_by_user_id=str(data.submitted_by_user_id),
        blackboard_entry_id=entry.id,
        specialist_type=data.specialist_type,
        proposal_kind=data.proposal_kind,
        title=data.title,
        problem_statement=data.problem_statement,
        recommendation=data.recommendation,
        rationale=data.rationale,
        expected_impact=data.expected_impact,
        confidence_level=data.confidence_level,
        severity=data.severity,
        evidence_json=json.dumps(data.evidence),
        risks_json=json.dumps(data.risks),
        status="submitted",
        target_artifact_id=target_artifact_id,
        target_artifact_version_id=target_artifact_version_id,
        target_decision_id=target_decision_id,
        target_creative_input_id=target_creative_input_id,
    )
    db.add(proposal)
    db.flush()
    _audit(
        db,
        entity_type="blackboard_entry",
        entity_id=entry.id,
        action="created",
        actor_user_id=entry.author_user_id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        payload={
            "entry_type": entry.entry_type,
            "title": entry.title,
            "status": entry.status,
            "severity": entry.severity,
            "source": "specialist_proposal",
        },
    )
    _audit(
        db,
        entity_type="specialist_proposal",
        entity_id=proposal.id,
        action="submitted",
        actor_user_id=proposal.submitted_by_user_id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        payload={
            "specialist_type": proposal.specialist_type,
            "proposal_kind": proposal.proposal_kind,
            "blackboard_entry_id": proposal.blackboard_entry_id,
        },
    )
    db.commit()
    db.refresh(proposal)
    return _specialist_proposal_read(proposal)


def list_project_specialist_proposals(
    db: Session,
    project_id: str,
    specialist_type: str | None = None,
) -> list[schemas.SpecialistProposalRead]:
    _one(db, models.Project, project_id)
    query = (
        select(models.SpecialistProposal)
        .where(models.SpecialistProposal.project_id == project_id)
        .order_by(models.SpecialistProposal.created_at)
    )
    if specialist_type is not None:
        query = query.where(models.SpecialistProposal.specialist_type == specialist_type)
    return [_specialist_proposal_read(proposal) for proposal in db.scalars(query).all()]


def get_specialist_proposal(
    db: Session, proposal_id: str
) -> schemas.SpecialistProposalRead:
    return _specialist_proposal_read(_one(db, models.SpecialistProposal, proposal_id))


def create_human_checkpoint(
    db: Session, project_id: str, data: schemas.HumanCheckpointCreate
) -> schemas.HumanCheckpointRead:
    project = _one(db, models.Project, project_id)
    _one(db, models.User, str(data.requested_by_user_id))

    linked_blackboard_entry_id = (
        str(data.linked_blackboard_entry_id) if data.linked_blackboard_entry_id else None
    )
    linked_deliberation_record_id = (
        str(data.linked_deliberation_record_id) if data.linked_deliberation_record_id else None
    )
    target_artifact_id = str(data.target_artifact_id) if data.target_artifact_id else None
    target_artifact_version_id = (
        str(data.target_artifact_version_id) if data.target_artifact_version_id else None
    )
    target_decision_id = str(data.target_decision_id) if data.target_decision_id else None
    target_creative_input_id = (
        str(data.target_creative_input_id) if data.target_creative_input_id else None
    )
    _validate_checkpoint_links(
        db,
        project=project,
        linked_blackboard_entry_id=linked_blackboard_entry_id,
        linked_deliberation_record_id=linked_deliberation_record_id,
    )
    _validate_blackboard_targets(
        db,
        project=project,
        target_artifact_id=target_artifact_id,
        target_artifact_version_id=target_artifact_version_id,
        target_decision_id=target_decision_id,
        target_creative_input_id=target_creative_input_id,
    )

    checkpoint = models.HumanCheckpoint(
        project_id=project.id,
        requested_by_user_id=str(data.requested_by_user_id),
        checkpoint_type=data.checkpoint_type,
        title=data.title,
        summary=data.summary,
        decision_status="pending",
        linked_blackboard_entry_id=linked_blackboard_entry_id,
        linked_deliberation_record_id=linked_deliberation_record_id,
        target_artifact_id=target_artifact_id,
        target_artifact_version_id=target_artifact_version_id,
        target_decision_id=target_decision_id,
        target_creative_input_id=target_creative_input_id,
    )
    db.add(checkpoint)
    db.flush()
    _audit(
        db,
        entity_type="human_checkpoint",
        entity_id=checkpoint.id,
        action="created",
        actor_user_id=checkpoint.requested_by_user_id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        payload={
            "checkpoint_type": checkpoint.checkpoint_type,
            "decision_status": checkpoint.decision_status,
            "title": checkpoint.title,
        },
    )
    db.commit()
    db.refresh(checkpoint)
    return _human_checkpoint_read(checkpoint)


def list_project_human_checkpoints(
    db: Session,
    project_id: str,
    checkpoint_type: str | None = None,
    decision_status: str | None = None,
) -> list[schemas.HumanCheckpointRead]:
    _one(db, models.Project, project_id)
    query = (
        select(models.HumanCheckpoint)
        .where(models.HumanCheckpoint.project_id == project_id)
        .order_by(models.HumanCheckpoint.created_at)
    )
    if checkpoint_type is not None:
        query = query.where(models.HumanCheckpoint.checkpoint_type == checkpoint_type)
    if decision_status is not None:
        query = query.where(models.HumanCheckpoint.decision_status == decision_status)
    return [_human_checkpoint_read(checkpoint) for checkpoint in db.scalars(query).all()]


def get_project_human_checkpoint_readiness(
    db: Session, project_id: str
) -> schemas.HumanCheckpointReadinessRead:
    project = _one(db, models.Project, project_id)
    checkpoints = db.scalars(
        select(models.HumanCheckpoint)
        .where(models.HumanCheckpoint.project_id == project.id)
        .order_by(models.HumanCheckpoint.created_at)
    ).all()

    latest_by_type: dict[str, models.HumanCheckpoint] = {}
    for checkpoint in checkpoints:
        latest_by_type[checkpoint.checkpoint_type] = checkpoint

    items = []
    approved = []
    missing = []
    blocked = []
    revision_requested = []
    for checkpoint_type in REQUIRED_HUMAN_CHECKPOINT_TYPES:
        checkpoint = latest_by_type.get(checkpoint_type)
        if checkpoint is None:
            missing.append(checkpoint_type)
            items.append(
                schemas.HumanCheckpointReadinessItem(
                    checkpoint_type=checkpoint_type,
                    status="missing",
                )
            )
            continue
        status = checkpoint.decision_status
        if status == "approved":
            approved.append(checkpoint_type)
        elif status == "blocked":
            blocked.append(checkpoint_type)
        elif status == "revision_requested":
            revision_requested.append(checkpoint_type)
        items.append(
            schemas.HumanCheckpointReadinessItem(
                checkpoint_type=checkpoint_type,
                status=status,
                checkpoint_id=checkpoint.id,
            )
        )

    return schemas.HumanCheckpointReadinessRead(
        project_id=project.id,
        ready=not missing and len(approved) == len(REQUIRED_HUMAN_CHECKPOINT_TYPES),
        required_checkpoint_types=REQUIRED_HUMAN_CHECKPOINT_TYPES,
        approved_checkpoint_types=approved,
        missing_checkpoint_types=missing,
        blocked_checkpoint_types=blocked,
        revision_requested_checkpoint_types=revision_requested,
        items=items,
    )


def get_human_checkpoint(db: Session, checkpoint_id: str) -> schemas.HumanCheckpointRead:
    return _human_checkpoint_read(_one(db, models.HumanCheckpoint, checkpoint_id))


def decide_human_checkpoint(
    db: Session, checkpoint_id: str, data: schemas.HumanCheckpointDecisionUpdate
) -> schemas.HumanCheckpointRead:
    checkpoint = _one(db, models.HumanCheckpoint, checkpoint_id)
    _one(db, models.User, str(data.decided_by_user_id))
    if checkpoint.decision_status != "pending":
        raise ConflictError("human checkpoint has already been decided; create a new checkpoint")
    old_status = checkpoint.decision_status
    checkpoint.decided_by_user_id = str(data.decided_by_user_id)
    checkpoint.decision_status = data.decision_status
    checkpoint.decision_rationale = data.decision_rationale
    db.flush()
    project = _one(db, models.Project, checkpoint.project_id)
    _audit(
        db,
        entity_type="human_checkpoint",
        entity_id=checkpoint.id,
        action="decided",
        actor_user_id=checkpoint.decided_by_user_id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        payload={
            "checkpoint_type": checkpoint.checkpoint_type,
            "old_status": old_status,
            "new_status": checkpoint.decision_status,
        },
    )
    db.commit()
    db.refresh(checkpoint)
    return _human_checkpoint_read(checkpoint)


def create_score_branch(
    db: Session, project_id: str, data: schemas.AudiovisualScoreBranchCreate
) -> schemas.AudiovisualScoreBranchRead:
    project = _one(db, models.Project, project_id)
    _one(db, models.User, str(data.created_by_user_id))
    source_artifact_version_id = (
        str(data.source_artifact_version_id) if data.source_artifact_version_id else None
    )
    source_decision_id = str(data.source_decision_id) if data.source_decision_id else None
    _validate_score_links(
        db,
        project=project,
        artifact_version_id=source_artifact_version_id,
        decision_id=source_decision_id,
    )

    branch = models.AudiovisualScoreBranch(
        project_id=project.id,
        created_by_user_id=str(data.created_by_user_id),
        name=data.name,
        purpose=data.purpose,
        status="draft",
        source_artifact_version_id=source_artifact_version_id,
        source_decision_id=source_decision_id,
    )
    db.add(branch)
    db.flush()
    _audit(
        db,
        entity_type="audiovisual_score_branch",
        entity_id=branch.id,
        action="created",
        actor_user_id=branch.created_by_user_id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        payload={"name": branch.name, "status": branch.status},
    )
    db.commit()
    db.refresh(branch)
    return _score_branch_read(branch)


def list_project_score_branches(
    db: Session, project_id: str
) -> list[schemas.AudiovisualScoreBranchRead]:
    _one(db, models.Project, project_id)
    branches = db.scalars(
        select(models.AudiovisualScoreBranch)
        .where(models.AudiovisualScoreBranch.project_id == project_id)
        .order_by(models.AudiovisualScoreBranch.created_at)
    ).all()
    return [_score_branch_read(branch) for branch in branches]


def get_score_branch(db: Session, branch_id: str) -> schemas.AudiovisualScoreBranchRead:
    return _score_branch_read(_one(db, models.AudiovisualScoreBranch, branch_id))


def create_score_event(
    db: Session, branch_id: str, data: schemas.AudiovisualScoreEventCreate
) -> schemas.AudiovisualScoreEventRead:
    branch = _one(db, models.AudiovisualScoreBranch, branch_id)
    project = _one(db, models.Project, branch.project_id)
    _one(db, models.User, str(data.created_by_user_id))

    parent_event_id = str(data.parent_event_id) if data.parent_event_id else None
    if parent_event_id is not None:
        parent = _one(db, models.AudiovisualScoreEvent, parent_event_id)
        if parent.branch_id != branch.id:
            raise ValidationError("parent score event does not belong to branch")

    linked_artifact_version_id = (
        str(data.linked_artifact_version_id) if data.linked_artifact_version_id else None
    )
    linked_decision_id = str(data.linked_decision_id) if data.linked_decision_id else None
    linked_blackboard_entry_id = (
        str(data.linked_blackboard_entry_id) if data.linked_blackboard_entry_id else None
    )
    _validate_score_links(
        db,
        project=project,
        artifact_version_id=linked_artifact_version_id,
        decision_id=linked_decision_id,
        blackboard_entry_id=linked_blackboard_entry_id,
    )

    event = models.AudiovisualScoreEvent(
        branch_id=branch.id,
        project_id=project.id,
        created_by_user_id=str(data.created_by_user_id),
        parent_event_id=parent_event_id,
        hierarchy_level=data.hierarchy_level,
        title=data.title,
        sort_key=data.sort_key,
        why=data.why,
        what=data.what,
        how=data.how,
        where_when_json=json.dumps(data.where_when.model_dump(), sort_keys=True),
        duration_policy=data.duration_policy,
        status=data.status,
        linked_artifact_version_id=linked_artifact_version_id,
        linked_decision_id=linked_decision_id,
        linked_blackboard_entry_id=linked_blackboard_entry_id,
    )
    db.add(event)
    db.flush()
    _audit(
        db,
        entity_type="audiovisual_score_event",
        entity_id=event.id,
        action="created",
        actor_user_id=event.created_by_user_id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        payload={
            "branch_id": event.branch_id,
            "hierarchy_level": event.hierarchy_level,
            "title": event.title,
            "status": event.status,
        },
    )
    db.commit()
    db.refresh(event)
    return _score_event_read(event)


def list_score_events(
    db: Session, branch_id: str
) -> list[schemas.AudiovisualScoreEventRead]:
    _one(db, models.AudiovisualScoreBranch, branch_id)
    events = db.scalars(
        select(models.AudiovisualScoreEvent)
        .where(models.AudiovisualScoreEvent.branch_id == branch_id)
        .order_by(models.AudiovisualScoreEvent.sort_key)
    ).all()
    return [_score_event_read(event) for event in events]


def get_score_event(db: Session, event_id: str) -> schemas.AudiovisualScoreEventRead:
    return _score_event_read(_one(db, models.AudiovisualScoreEvent, event_id))


def create_score_lane_entry(
    db: Session, event_id: str, data: schemas.AudiovisualScoreLaneEntryCreate
) -> schemas.AudiovisualScoreLaneEntryRead:
    score_event = _one(db, models.AudiovisualScoreEvent, event_id)
    project = _one(db, models.Project, score_event.project_id)
    _one(db, models.User, str(data.created_by_user_id))

    linked_artifact_version_id = (
        str(data.linked_artifact_version_id) if data.linked_artifact_version_id else None
    )
    linked_decision_id = str(data.linked_decision_id) if data.linked_decision_id else None
    linked_blackboard_entry_id = (
        str(data.linked_blackboard_entry_id) if data.linked_blackboard_entry_id else None
    )
    _validate_score_links(
        db,
        project=project,
        artifact_version_id=linked_artifact_version_id,
        decision_id=linked_decision_id,
        blackboard_entry_id=linked_blackboard_entry_id,
    )

    entry = models.AudiovisualScoreLaneEntry(
        branch_id=score_event.branch_id,
        score_event_id=score_event.id,
        project_id=project.id,
        created_by_user_id=str(data.created_by_user_id),
        lane_type=data.lane_type,
        title=data.title,
        intent=data.intent,
        content_json=json.dumps(data.content, sort_keys=True),
        status=data.status,
        linked_artifact_version_id=linked_artifact_version_id,
        linked_decision_id=linked_decision_id,
        linked_blackboard_entry_id=linked_blackboard_entry_id,
    )
    db.add(entry)
    db.flush()
    _audit(
        db,
        entity_type="audiovisual_score_lane_entry",
        entity_id=entry.id,
        action="created",
        actor_user_id=entry.created_by_user_id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        payload={
            "score_event_id": entry.score_event_id,
            "lane_type": entry.lane_type,
            "title": entry.title,
            "status": entry.status,
        },
    )
    db.commit()
    db.refresh(entry)
    return _score_lane_entry_read(entry)


def list_score_event_lane_entries(
    db: Session, event_id: str, lane_type: str | None = None
) -> list[schemas.AudiovisualScoreLaneEntryRead]:
    _one(db, models.AudiovisualScoreEvent, event_id)
    query = (
        select(models.AudiovisualScoreLaneEntry)
        .where(models.AudiovisualScoreLaneEntry.score_event_id == event_id)
        .order_by(models.AudiovisualScoreLaneEntry.created_at)
    )
    if lane_type is not None:
        query = query.where(models.AudiovisualScoreLaneEntry.lane_type == lane_type)
    return [_score_lane_entry_read(entry) for entry in db.scalars(query).all()]


def list_score_branch_lane_entries(
    db: Session, branch_id: str, lane_type: str | None = None
) -> list[schemas.AudiovisualScoreLaneEntryRead]:
    _one(db, models.AudiovisualScoreBranch, branch_id)
    query = (
        select(models.AudiovisualScoreLaneEntry)
        .where(models.AudiovisualScoreLaneEntry.branch_id == branch_id)
        .order_by(models.AudiovisualScoreLaneEntry.created_at)
    )
    if lane_type is not None:
        query = query.where(models.AudiovisualScoreLaneEntry.lane_type == lane_type)
    return [_score_lane_entry_read(entry) for entry in db.scalars(query).all()]


def get_score_lane_entry(
    db: Session, lane_entry_id: str
) -> schemas.AudiovisualScoreLaneEntryRead:
    return _score_lane_entry_read(_one(db, models.AudiovisualScoreLaneEntry, lane_entry_id))


def create_score_event_relationship(
    db: Session, from_event_id: str, data: schemas.AudiovisualScoreEventRelationshipCreate
) -> schemas.AudiovisualScoreEventRelationshipRead:
    from_event = _one(db, models.AudiovisualScoreEvent, from_event_id)
    to_event = _one(db, models.AudiovisualScoreEvent, str(data.to_event_id))
    if from_event.id == to_event.id:
        raise ValidationError("score event relationship cannot point to itself")
    if from_event.branch_id != to_event.branch_id:
        raise ValidationError("score event relationship requires events in the same branch")

    project = _one(db, models.Project, from_event.project_id)
    _one(db, models.User, str(data.created_by_user_id))

    linked_artifact_version_id = (
        str(data.linked_artifact_version_id) if data.linked_artifact_version_id else None
    )
    linked_decision_id = str(data.linked_decision_id) if data.linked_decision_id else None
    linked_blackboard_entry_id = (
        str(data.linked_blackboard_entry_id) if data.linked_blackboard_entry_id else None
    )
    _validate_score_links(
        db,
        project=project,
        artifact_version_id=linked_artifact_version_id,
        decision_id=linked_decision_id,
        blackboard_entry_id=linked_blackboard_entry_id,
    )

    relationship = models.AudiovisualScoreEventRelationship(
        branch_id=from_event.branch_id,
        project_id=project.id,
        created_by_user_id=str(data.created_by_user_id),
        from_event_id=from_event.id,
        to_event_id=to_event.id,
        relationship_type=data.relationship_type,
        title=data.title,
        rationale=data.rationale,
        expected_viewer_effect=data.expected_viewer_effect,
        timing_logic=data.timing_logic,
        continuity_impact=data.continuity_impact,
        status=data.status,
        linked_artifact_version_id=linked_artifact_version_id,
        linked_decision_id=linked_decision_id,
        linked_blackboard_entry_id=linked_blackboard_entry_id,
    )
    db.add(relationship)
    db.flush()
    _audit(
        db,
        entity_type="audiovisual_score_event_relationship",
        entity_id=relationship.id,
        action="created",
        actor_user_id=relationship.created_by_user_id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        payload={
            "from_event_id": relationship.from_event_id,
            "to_event_id": relationship.to_event_id,
            "relationship_type": relationship.relationship_type,
            "status": relationship.status,
        },
    )
    db.commit()
    db.refresh(relationship)
    return _score_event_relationship_read(relationship)


def list_score_event_relationships(
    db: Session, event_id: str, direction: str = "outgoing"
) -> list[schemas.AudiovisualScoreEventRelationshipRead]:
    _one(db, models.AudiovisualScoreEvent, event_id)
    query = select(models.AudiovisualScoreEventRelationship)
    if direction == "outgoing":
        query = query.where(models.AudiovisualScoreEventRelationship.from_event_id == event_id)
    elif direction == "incoming":
        query = query.where(models.AudiovisualScoreEventRelationship.to_event_id == event_id)
    else:
        query = query.where(
            (models.AudiovisualScoreEventRelationship.from_event_id == event_id)
            | (models.AudiovisualScoreEventRelationship.to_event_id == event_id)
        )
    relationships = db.scalars(query.order_by(models.AudiovisualScoreEventRelationship.created_at)).all()
    return [_score_event_relationship_read(relationship) for relationship in relationships]


def list_score_branch_relationships(
    db: Session, branch_id: str, relationship_type: str | None = None
) -> list[schemas.AudiovisualScoreEventRelationshipRead]:
    _one(db, models.AudiovisualScoreBranch, branch_id)
    query = (
        select(models.AudiovisualScoreEventRelationship)
        .where(models.AudiovisualScoreEventRelationship.branch_id == branch_id)
        .order_by(models.AudiovisualScoreEventRelationship.created_at)
    )
    if relationship_type is not None:
        query = query.where(
            models.AudiovisualScoreEventRelationship.relationship_type == relationship_type
        )
    return [
        _score_event_relationship_read(relationship)
        for relationship in db.scalars(query).all()
    ]


def get_score_event_relationship(
    db: Session, relationship_id: str
) -> schemas.AudiovisualScoreEventRelationshipRead:
    return _score_event_relationship_read(
        _one(db, models.AudiovisualScoreEventRelationship, relationship_id)
    )


def create_score_preview_prototype(
    db: Session, branch_id: str, data: schemas.AudiovisualScorePreviewPrototypeCreate
) -> schemas.AudiovisualScorePreviewPrototypeRead:
    branch = _one(db, models.AudiovisualScoreBranch, branch_id)
    project = _one(db, models.Project, branch.project_id)
    _one(db, models.User, str(data.created_by_user_id))
    linked_decision_id = str(data.linked_decision_id) if data.linked_decision_id else None
    linked_blackboard_entry_id = (
        str(data.linked_blackboard_entry_id) if data.linked_blackboard_entry_id else None
    )
    _validate_score_links(
        db,
        project=project,
        decision_id=linked_decision_id,
        blackboard_entry_id=linked_blackboard_entry_id,
    )

    prototype = models.AudiovisualScorePreviewPrototype(
        branch_id=branch.id,
        project_id=project.id,
        created_by_user_id=str(data.created_by_user_id),
        prototype_type=data.prototype_type,
        title=data.title,
        purpose=data.purpose,
        test_question=data.test_question,
        status="draft",
        linked_decision_id=linked_decision_id,
        linked_blackboard_entry_id=linked_blackboard_entry_id,
    )
    db.add(prototype)
    db.flush()
    _audit(
        db,
        entity_type="audiovisual_score_preview_prototype",
        entity_id=prototype.id,
        action="created",
        actor_user_id=prototype.created_by_user_id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        payload={
            "branch_id": prototype.branch_id,
            "prototype_type": prototype.prototype_type,
            "status": prototype.status,
        },
    )
    db.commit()
    db.refresh(prototype)
    return _score_preview_prototype_read(prototype)


def list_score_branch_preview_prototypes(
    db: Session, branch_id: str
) -> list[schemas.AudiovisualScorePreviewPrototypeRead]:
    _one(db, models.AudiovisualScoreBranch, branch_id)
    prototypes = db.scalars(
        select(models.AudiovisualScorePreviewPrototype)
        .where(models.AudiovisualScorePreviewPrototype.branch_id == branch_id)
        .order_by(models.AudiovisualScorePreviewPrototype.created_at)
    ).all()
    return [_score_preview_prototype_read(prototype) for prototype in prototypes]


def get_score_preview_prototype(
    db: Session, prototype_id: str
) -> schemas.AudiovisualScorePreviewPrototypeRead:
    return _score_preview_prototype_read(
        _one(db, models.AudiovisualScorePreviewPrototype, prototype_id)
    )


def create_score_preview_item(
    db: Session, prototype_id: str, data: schemas.AudiovisualScorePreviewItemCreate
) -> schemas.AudiovisualScorePreviewItemRead:
    prototype = _one(db, models.AudiovisualScorePreviewPrototype, prototype_id)
    score_event = _one(db, models.AudiovisualScoreEvent, str(data.score_event_id))
    if score_event.branch_id != prototype.branch_id:
        raise ValidationError("preview item score event must belong to prototype branch")

    project = _one(db, models.Project, prototype.project_id)
    _one(db, models.User, str(data.created_by_user_id))
    linked_artifact_version_id = (
        str(data.linked_artifact_version_id) if data.linked_artifact_version_id else None
    )
    linked_decision_id = str(data.linked_decision_id) if data.linked_decision_id else None
    linked_blackboard_entry_id = (
        str(data.linked_blackboard_entry_id) if data.linked_blackboard_entry_id else None
    )
    _validate_score_links(
        db,
        project=project,
        artifact_version_id=linked_artifact_version_id,
        decision_id=linked_decision_id,
        blackboard_entry_id=linked_blackboard_entry_id,
    )

    item = models.AudiovisualScorePreviewItem(
        prototype_id=prototype.id,
        branch_id=prototype.branch_id,
        score_event_id=score_event.id,
        project_id=project.id,
        created_by_user_id=str(data.created_by_user_id),
        item_type=data.item_type,
        title=data.title,
        sort_key=data.sort_key,
        test_focus=data.test_focus,
        inspection_notes=data.inspection_notes,
        score_event_why_snapshot=score_event.why,
        body_json=json.dumps(data.body, sort_keys=True),
        status=data.status,
        linked_artifact_version_id=linked_artifact_version_id,
        linked_decision_id=linked_decision_id,
        linked_blackboard_entry_id=linked_blackboard_entry_id,
    )
    db.add(item)
    db.flush()
    _audit(
        db,
        entity_type="audiovisual_score_preview_item",
        entity_id=item.id,
        action="created",
        actor_user_id=item.created_by_user_id,
        workspace_id=project.workspace_id,
        project_id=project.id,
        payload={
            "prototype_id": item.prototype_id,
            "score_event_id": item.score_event_id,
            "item_type": item.item_type,
            "status": item.status,
        },
    )
    db.commit()
    db.refresh(item)
    return _score_preview_item_read(item)


def list_score_preview_items(
    db: Session, prototype_id: str, item_type: str | None = None
) -> list[schemas.AudiovisualScorePreviewItemRead]:
    _one(db, models.AudiovisualScorePreviewPrototype, prototype_id)
    query = (
        select(models.AudiovisualScorePreviewItem)
        .where(models.AudiovisualScorePreviewItem.prototype_id == prototype_id)
        .order_by(models.AudiovisualScorePreviewItem.sort_key)
    )
    if item_type is not None:
        query = query.where(models.AudiovisualScorePreviewItem.item_type == item_type)
    return [_score_preview_item_read(item) for item in db.scalars(query).all()]


def get_score_preview_item(
    db: Session, preview_item_id: str
) -> schemas.AudiovisualScorePreviewItemRead:
    return _score_preview_item_read(_one(db, models.AudiovisualScorePreviewItem, preview_item_id))


def get_score_preview_coverage(
    db: Session, prototype_id: str
) -> schemas.AudiovisualScorePreviewCoverageRead:
    prototype = _one(db, models.AudiovisualScorePreviewPrototype, prototype_id)
    score_events = db.scalars(
        select(models.AudiovisualScoreEvent)
        .where(models.AudiovisualScoreEvent.branch_id == prototype.branch_id)
        .order_by(models.AudiovisualScoreEvent.sort_key)
    ).all()
    preview_items = db.scalars(
        select(models.AudiovisualScorePreviewItem).where(
            models.AudiovisualScorePreviewItem.prototype_id == prototype.id
        )
    ).all()
    item_counts: dict[str, int] = {}
    for item in preview_items:
        item_counts[item.score_event_id] = item_counts.get(item.score_event_id, 0) + 1

    events = []
    missing_score_event_ids = []
    for score_event in score_events:
        item_count = item_counts.get(score_event.id, 0)
        covered = item_count > 0
        if not covered:
            missing_score_event_ids.append(score_event.id)
        events.append(
            schemas.AudiovisualScorePreviewCoverageEventRead(
                score_event_id=score_event.id,
                title=score_event.title,
                sort_key=score_event.sort_key,
                why=score_event.why,
                preview_item_count=item_count,
                covered=covered,
            )
        )

    return schemas.AudiovisualScorePreviewCoverageRead(
        prototype_id=prototype.id,
        branch_id=prototype.branch_id,
        project_id=prototype.project_id,
        ready=bool(score_events) and not missing_score_event_ids,
        total_score_events=len(score_events),
        covered_score_events=len(score_events) - len(missing_score_event_ids),
        missing_score_event_ids=missing_score_event_ids,
        events=events,
    )
