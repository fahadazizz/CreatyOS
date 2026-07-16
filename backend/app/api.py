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
        raise HTTPException(status_code=422, detail=str(exc)) from exc
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


@router.post(
    "/projects/{project_id}/decisions",
    response_model=schemas.DecisionRead,
    status_code=201,
)
async def create_decision(
    project_id: UUID, payload: schemas.DecisionCreate, db: Session = Depends(get_db)
):
    try:
        return services.create_decision(db, str(project_id), payload)
    except Exception as exc:
        _handle_error(exc)


@router.get("/projects/{project_id}/decisions", response_model=list[schemas.DecisionRead])
async def list_project_decisions(project_id: UUID, db: Session = Depends(get_db)):
    try:
        return services.list_project_decisions(db, str(project_id))
    except Exception as exc:
        _handle_error(exc)


@router.get("/decisions/{decision_id}", response_model=schemas.DecisionRead)
async def get_decision(decision_id: UUID, db: Session = Depends(get_db)):
    try:
        return services.get_decision(db, str(decision_id))
    except Exception as exc:
        _handle_error(exc)


@router.patch("/decisions/{decision_id}/status", response_model=schemas.DecisionRead)
async def update_decision_status(
    decision_id: UUID, payload: schemas.DecisionStatusUpdate, db: Session = Depends(get_db)
):
    try:
        return services.update_decision_status(db, str(decision_id), payload)
    except Exception as exc:
        _handle_error(exc)


@router.post(
    "/projects/{project_id}/creative-inputs",
    response_model=schemas.CreativeInputRead,
    status_code=201,
)
async def create_creative_input(
    project_id: UUID, payload: schemas.CreativeInputCreate, db: Session = Depends(get_db)
):
    try:
        return services.create_creative_input(db, str(project_id), payload)
    except Exception as exc:
        _handle_error(exc)


@router.get(
    "/projects/{project_id}/creative-inputs",
    response_model=list[schemas.CreativeInputRead],
)
async def list_project_creative_inputs(
    project_id: UUID,
    input_type: schemas.CreativeInputType | None = Query(default=None),
    db: Session = Depends(get_db),
):
    try:
        return services.list_project_creative_inputs(
            db, str(project_id), input_type=input_type
        )
    except Exception as exc:
        _handle_error(exc)


@router.get("/creative-inputs/{creative_input_id}", response_model=schemas.CreativeInputRead)
async def get_creative_input(creative_input_id: UUID, db: Session = Depends(get_db)):
    try:
        return services.get_creative_input(db, str(creative_input_id))
    except Exception as exc:
        _handle_error(exc)


@router.post(
    "/projects/{project_id}/blackboard-entries",
    response_model=schemas.BlackboardEntryRead,
    status_code=201,
)
async def create_blackboard_entry(
    project_id: UUID, payload: schemas.BlackboardEntryCreate, db: Session = Depends(get_db)
):
    try:
        return services.create_blackboard_entry(db, str(project_id), payload)
    except Exception as exc:
        _handle_error(exc)


@router.get(
    "/projects/{project_id}/blackboard-entries",
    response_model=list[schemas.BlackboardEntryRead],
)
async def list_project_blackboard_entries(
    project_id: UUID,
    entry_type: schemas.BlackboardEntryType | None = Query(default=None),
    status: schemas.BlackboardEntryStatus | None = Query(default=None),
    db: Session = Depends(get_db),
):
    try:
        return services.list_project_blackboard_entries(
            db, str(project_id), entry_type=entry_type, status=status
        )
    except Exception as exc:
        _handle_error(exc)


@router.get("/blackboard-entries/{entry_id}", response_model=schemas.BlackboardEntryRead)
async def get_blackboard_entry(entry_id: UUID, db: Session = Depends(get_db)):
    try:
        return services.get_blackboard_entry(db, str(entry_id))
    except Exception as exc:
        _handle_error(exc)


@router.patch(
    "/blackboard-entries/{entry_id}/status",
    response_model=schemas.BlackboardEntryRead,
)
async def update_blackboard_entry_status(
    entry_id: UUID,
    payload: schemas.BlackboardEntryStatusUpdate,
    db: Session = Depends(get_db),
):
    try:
        return services.update_blackboard_entry_status(db, str(entry_id), payload)
    except Exception as exc:
        _handle_error(exc)


@router.post(
    "/projects/{project_id}/deliberations",
    response_model=schemas.DeliberationRecordRead,
    status_code=201,
)
async def create_deliberation_record(
    project_id: UUID,
    payload: schemas.DeliberationRecordCreate,
    db: Session = Depends(get_db),
):
    try:
        return services.create_deliberation_record(db, str(project_id), payload)
    except Exception as exc:
        _handle_error(exc)


@router.post(
    "/projects/{project_id}/deliberation-controller-runs",
    response_model=schemas.DeliberationControllerRunRead,
    status_code=201,
)
async def run_deliberation_controller(
    project_id: UUID,
    payload: schemas.DeliberationControllerRunCreate,
    db: Session = Depends(get_db),
):
    try:
        return services.run_deliberation_controller(db, str(project_id), payload)
    except Exception as exc:
        _handle_error(exc)


@router.get(
    "/projects/{project_id}/deliberations",
    response_model=list[schemas.DeliberationRecordRead],
)
async def list_project_deliberation_records(
    project_id: UUID, db: Session = Depends(get_db)
):
    try:
        return services.list_project_deliberation_records(db, str(project_id))
    except Exception as exc:
        _handle_error(exc)


@router.get("/deliberations/{deliberation_id}", response_model=schemas.DeliberationRecordRead)
async def get_deliberation_record(deliberation_id: UUID, db: Session = Depends(get_db)):
    try:
        return services.get_deliberation_record(db, str(deliberation_id))
    except Exception as exc:
        _handle_error(exc)


@router.post(
    "/projects/{project_id}/specialist-proposals",
    response_model=schemas.SpecialistProposalRead,
    status_code=201,
)
async def create_specialist_proposal(
    project_id: UUID,
    payload: schemas.SpecialistProposalCreate,
    db: Session = Depends(get_db),
):
    try:
        return services.create_specialist_proposal(db, str(project_id), payload)
    except Exception as exc:
        _handle_error(exc)


@router.get(
    "/projects/{project_id}/specialist-proposals",
    response_model=list[schemas.SpecialistProposalRead],
)
async def list_project_specialist_proposals(
    project_id: UUID,
    specialist_type: schemas.SpecialistType | None = Query(default=None),
    db: Session = Depends(get_db),
):
    try:
        return services.list_project_specialist_proposals(
            db, str(project_id), specialist_type=specialist_type
        )
    except Exception as exc:
        _handle_error(exc)


@router.get(
    "/specialist-proposals/{proposal_id}",
    response_model=schemas.SpecialistProposalRead,
)
async def get_specialist_proposal(proposal_id: UUID, db: Session = Depends(get_db)):
    try:
        return services.get_specialist_proposal(db, str(proposal_id))
    except Exception as exc:
        _handle_error(exc)


@router.post(
    "/projects/{project_id}/human-checkpoints",
    response_model=schemas.HumanCheckpointRead,
    status_code=201,
)
async def create_human_checkpoint(
    project_id: UUID,
    payload: schemas.HumanCheckpointCreate,
    db: Session = Depends(get_db),
):
    try:
        return services.create_human_checkpoint(db, str(project_id), payload)
    except Exception as exc:
        _handle_error(exc)


@router.get(
    "/projects/{project_id}/human-checkpoints",
    response_model=list[schemas.HumanCheckpointRead],
)
async def list_project_human_checkpoints(
    project_id: UUID,
    checkpoint_type: schemas.HumanCheckpointType | None = Query(default=None),
    decision_status: schemas.HumanCheckpointStatus | None = Query(default=None),
    db: Session = Depends(get_db),
):
    try:
        return services.list_project_human_checkpoints(
            db,
            str(project_id),
            checkpoint_type=checkpoint_type,
            decision_status=decision_status,
        )
    except Exception as exc:
        _handle_error(exc)


@router.get("/human-checkpoints/{checkpoint_id}", response_model=schemas.HumanCheckpointRead)
async def get_human_checkpoint(checkpoint_id: UUID, db: Session = Depends(get_db)):
    try:
        return services.get_human_checkpoint(db, str(checkpoint_id))
    except Exception as exc:
        _handle_error(exc)


@router.patch(
    "/human-checkpoints/{checkpoint_id}/decision",
    response_model=schemas.HumanCheckpointRead,
)
async def decide_human_checkpoint(
    checkpoint_id: UUID,
    payload: schemas.HumanCheckpointDecisionUpdate,
    db: Session = Depends(get_db),
):
    try:
        return services.decide_human_checkpoint(db, str(checkpoint_id), payload)
    except Exception as exc:
        _handle_error(exc)
