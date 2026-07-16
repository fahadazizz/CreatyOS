import json
from typing import Any

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

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
        body_json=json.dumps(data.body, sort_keys=True),
        linked_decisions_json=json.dumps([str(item) for item in data.linked_decisions]),
        linked_evidence_json=json.dumps(data.linked_evidence),
        open_questions_json=json.dumps(data.open_questions),
    )
    db.add(version)
    db.flush()
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
