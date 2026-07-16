from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import schemas, services
from app.db import get_db

router = APIRouter(prefix="/api/v1")


def _handle_error(exc: Exception) -> None:
    if isinstance(exc, services.NotFoundError):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    if isinstance(exc, services.ConflictError):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc
    if isinstance(exc, services.ValidationError):
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(exc)) from exc
    raise exc


@router.post("/workspaces", response_model=schemas.WorkspaceRead, status_code=201)
async def create_workspace(payload: schemas.WorkspaceCreate, db: Session = Depends(get_db)):
    try:
        return services.create_workspace(db, payload)
    except Exception as exc:
        _handle_error(exc)


@router.post("/users", response_model=schemas.UserRead, status_code=201)
async def create_user(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        return services.create_user(db, payload)
    except Exception as exc:
        _handle_error(exc)


@router.post("/projects", response_model=schemas.ProjectRead, status_code=201)
async def create_project(payload: schemas.ProjectCreate, db: Session = Depends(get_db)):
    try:
        return services.create_project(db, payload)
    except Exception as exc:
        _handle_error(exc)


@router.get("/projects", response_model=list[schemas.ProjectRead])
async def list_projects(db: Session = Depends(get_db)):
    return services.list_projects(db)


@router.get("/projects/{project_id}", response_model=schemas.ProjectRead)
async def get_project(project_id: UUID, db: Session = Depends(get_db)):
    try:
        return services.get_project(db, str(project_id))
    except Exception as exc:
        _handle_error(exc)


@router.post(
    "/projects/{project_id}/productions",
    response_model=schemas.ProductionRead,
    status_code=201,
)
async def create_production(
    project_id: UUID, payload: schemas.ProductionCreate, db: Session = Depends(get_db)
):
    try:
        return services.create_production(db, str(project_id), payload)
    except Exception as exc:
        _handle_error(exc)


@router.post(
    "/productions/{production_id}/pieces",
    response_model=schemas.PieceRead,
    status_code=201,
)
async def create_piece(
    production_id: UUID, payload: schemas.PieceCreate, db: Session = Depends(get_db)
):
    try:
        return services.create_piece(db, str(production_id), payload)
    except Exception as exc:
        _handle_error(exc)


@router.post(
    "/pieces/{piece_id}/deliverables",
    response_model=schemas.DeliverableRead,
    status_code=201,
)
async def create_deliverable(
    piece_id: UUID, payload: schemas.DeliverableCreate, db: Session = Depends(get_db)
):
    try:
        return services.create_deliverable(db, str(piece_id), payload)
    except Exception as exc:
        _handle_error(exc)


@router.get("/audit-events", response_model=list[schemas.AuditEventRead])
async def list_audit_events(
    project_id: UUID | None = Query(default=None), db: Session = Depends(get_db)
):
    return services.list_audit_events(db, str(project_id) if project_id else None)


@router.post(
    "/projects/{project_id}/artifacts",
    response_model=schemas.ArtifactRead,
    status_code=201,
)
async def create_artifact(
    project_id: UUID, payload: schemas.ArtifactCreate, db: Session = Depends(get_db)
):
    try:
        return services.create_artifact(db, str(project_id), payload)
    except Exception as exc:
        _handle_error(exc)


@router.get("/projects/{project_id}/artifacts", response_model=list[schemas.ArtifactRead])
async def list_project_artifacts(project_id: UUID, db: Session = Depends(get_db)):
    try:
        return services.list_project_artifacts(db, str(project_id))
    except Exception as exc:
        _handle_error(exc)


@router.get("/artifacts/{artifact_id}", response_model=schemas.ArtifactRead)
async def get_artifact(artifact_id: UUID, db: Session = Depends(get_db)):
    try:
        return services.get_artifact(db, str(artifact_id))
    except Exception as exc:
        _handle_error(exc)


@router.post(
    "/artifacts/{artifact_id}/versions",
    response_model=schemas.ArtifactVersionRead,
    status_code=201,
)
async def create_artifact_version(
    artifact_id: UUID, payload: schemas.ArtifactVersionCreate, db: Session = Depends(get_db)
):
    try:
        return services.create_artifact_version(db, str(artifact_id), payload)
    except Exception as exc:
        _handle_error(exc)


@router.get(
    "/artifacts/{artifact_id}/versions",
    response_model=list[schemas.ArtifactVersionRead],
)
async def list_artifact_versions(artifact_id: UUID, db: Session = Depends(get_db)):
    try:
        return services.list_artifact_versions(db, str(artifact_id))
    except Exception as exc:
        _handle_error(exc)
