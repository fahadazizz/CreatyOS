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
