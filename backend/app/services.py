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
