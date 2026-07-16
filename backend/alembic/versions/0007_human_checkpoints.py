"""human checkpoints

Revision ID: 0007_human_checkpoints
Revises: 0006_specialist_proposals
Create Date: 2026-07-16
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0007_human_checkpoints"
down_revision: str | None = "0006_specialist_proposals"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "human_checkpoints",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("requested_by_user_id", sa.String(length=36), nullable=False),
        sa.Column("decided_by_user_id", sa.String(length=36), nullable=True),
        sa.Column("checkpoint_type", sa.String(length=80), nullable=False),
        sa.Column("title", sa.String(length=240), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("decision_status", sa.String(length=40), nullable=False),
        sa.Column("decision_rationale", sa.Text(), nullable=True),
        sa.Column("linked_blackboard_entry_id", sa.String(length=36), nullable=True),
        sa.Column("linked_deliberation_record_id", sa.String(length=36), nullable=True),
        sa.Column("target_artifact_id", sa.String(length=36), nullable=True),
        sa.Column("target_artifact_version_id", sa.String(length=36), nullable=True),
        sa.Column("target_decision_id", sa.String(length=36), nullable=True),
        sa.Column("target_creative_input_id", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["decided_by_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["linked_blackboard_entry_id"], ["blackboard_entries.id"]),
        sa.ForeignKeyConstraint(["linked_deliberation_record_id"], ["deliberation_records.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.ForeignKeyConstraint(["requested_by_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["target_artifact_id"], ["artifacts.id"]),
        sa.ForeignKeyConstraint(["target_artifact_version_id"], ["artifact_versions.id"]),
        sa.ForeignKeyConstraint(["target_creative_input_id"], ["creative_inputs.id"]),
        sa.ForeignKeyConstraint(["target_decision_id"], ["decisions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    for column in (
        "checkpoint_type",
        "decided_by_user_id",
        "decision_status",
        "linked_blackboard_entry_id",
        "linked_deliberation_record_id",
        "project_id",
        "requested_by_user_id",
        "target_artifact_id",
        "target_artifact_version_id",
        "target_creative_input_id",
        "target_decision_id",
    ):
        op.create_index(op.f(f"ix_human_checkpoints_{column}"), "human_checkpoints", [column])


def downgrade() -> None:
    for column in (
        "target_decision_id",
        "target_creative_input_id",
        "target_artifact_version_id",
        "target_artifact_id",
        "requested_by_user_id",
        "project_id",
        "linked_deliberation_record_id",
        "linked_blackboard_entry_id",
        "decision_status",
        "decided_by_user_id",
        "checkpoint_type",
    ):
        op.drop_index(op.f(f"ix_human_checkpoints_{column}"), table_name="human_checkpoints")
    op.drop_table("human_checkpoints")
