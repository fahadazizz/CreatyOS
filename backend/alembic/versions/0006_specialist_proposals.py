"""specialist proposals

Revision ID: 0006_specialist_proposals
Revises: 0005_studio_brain_blackboard
Create Date: 2026-07-16
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0006_specialist_proposals"
down_revision: str | None = "0005_studio_brain_blackboard"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "specialist_proposals",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("submitted_by_user_id", sa.String(length=36), nullable=False),
        sa.Column("blackboard_entry_id", sa.String(length=36), nullable=False),
        sa.Column("specialist_type", sa.String(length=80), nullable=False),
        sa.Column("proposal_kind", sa.String(length=80), nullable=False),
        sa.Column("title", sa.String(length=240), nullable=False),
        sa.Column("problem_statement", sa.Text(), nullable=False),
        sa.Column("recommendation", sa.Text(), nullable=False),
        sa.Column("rationale", sa.Text(), nullable=False),
        sa.Column("expected_impact", sa.Text(), nullable=False),
        sa.Column("confidence_level", sa.String(length=40), nullable=False),
        sa.Column("severity", sa.String(length=40), nullable=False),
        sa.Column("evidence_json", sa.Text(), nullable=False),
        sa.Column("risks_json", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("target_artifact_id", sa.String(length=36), nullable=True),
        sa.Column("target_artifact_version_id", sa.String(length=36), nullable=True),
        sa.Column("target_decision_id", sa.String(length=36), nullable=True),
        sa.Column("target_creative_input_id", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["blackboard_entry_id"], ["blackboard_entries.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.ForeignKeyConstraint(["submitted_by_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["target_artifact_id"], ["artifacts.id"]),
        sa.ForeignKeyConstraint(["target_artifact_version_id"], ["artifact_versions.id"]),
        sa.ForeignKeyConstraint(["target_creative_input_id"], ["creative_inputs.id"]),
        sa.ForeignKeyConstraint(["target_decision_id"], ["decisions.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("blackboard_entry_id"),
    )
    op.create_index(
        op.f("ix_specialist_proposals_blackboard_entry_id"),
        "specialist_proposals",
        ["blackboard_entry_id"],
        unique=True,
    )
    op.create_index(
        op.f("ix_specialist_proposals_project_id"),
        "specialist_proposals",
        ["project_id"],
    )
    op.create_index(
        op.f("ix_specialist_proposals_proposal_kind"),
        "specialist_proposals",
        ["proposal_kind"],
    )
    op.create_index(
        op.f("ix_specialist_proposals_specialist_type"),
        "specialist_proposals",
        ["specialist_type"],
    )
    op.create_index(
        op.f("ix_specialist_proposals_status"),
        "specialist_proposals",
        ["status"],
    )
    op.create_index(
        op.f("ix_specialist_proposals_submitted_by_user_id"),
        "specialist_proposals",
        ["submitted_by_user_id"],
    )
    op.create_index(
        op.f("ix_specialist_proposals_target_artifact_id"),
        "specialist_proposals",
        ["target_artifact_id"],
    )
    op.create_index(
        op.f("ix_specialist_proposals_target_artifact_version_id"),
        "specialist_proposals",
        ["target_artifact_version_id"],
    )
    op.create_index(
        op.f("ix_specialist_proposals_target_creative_input_id"),
        "specialist_proposals",
        ["target_creative_input_id"],
    )
    op.create_index(
        op.f("ix_specialist_proposals_target_decision_id"),
        "specialist_proposals",
        ["target_decision_id"],
    )


def downgrade() -> None:
    op.drop_index(
        op.f("ix_specialist_proposals_target_decision_id"),
        table_name="specialist_proposals",
    )
    op.drop_index(
        op.f("ix_specialist_proposals_target_creative_input_id"),
        table_name="specialist_proposals",
    )
    op.drop_index(
        op.f("ix_specialist_proposals_target_artifact_version_id"),
        table_name="specialist_proposals",
    )
    op.drop_index(
        op.f("ix_specialist_proposals_target_artifact_id"),
        table_name="specialist_proposals",
    )
    op.drop_index(
        op.f("ix_specialist_proposals_submitted_by_user_id"),
        table_name="specialist_proposals",
    )
    op.drop_index(op.f("ix_specialist_proposals_status"), table_name="specialist_proposals")
    op.drop_index(
        op.f("ix_specialist_proposals_specialist_type"),
        table_name="specialist_proposals",
    )
    op.drop_index(
        op.f("ix_specialist_proposals_proposal_kind"),
        table_name="specialist_proposals",
    )
    op.drop_index(op.f("ix_specialist_proposals_project_id"), table_name="specialist_proposals")
    op.drop_index(
        op.f("ix_specialist_proposals_blackboard_entry_id"),
        table_name="specialist_proposals",
    )
    op.drop_table("specialist_proposals")
