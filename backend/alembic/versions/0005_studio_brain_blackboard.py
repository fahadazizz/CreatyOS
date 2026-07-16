"""studio brain blackboard

Revision ID: 0005_studio_brain_blackboard
Revises: 0004_creative_inputs
Create Date: 2026-07-16
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0005_studio_brain_blackboard"
down_revision: str | None = "0004_creative_inputs"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "blackboard_entries",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("author_user_id", sa.String(length=36), nullable=False),
        sa.Column("entry_type", sa.String(length=80), nullable=False),
        sa.Column("title", sa.String(length=240), nullable=False),
        sa.Column("summary", sa.Text(), nullable=False),
        sa.Column("rationale", sa.Text(), nullable=False),
        sa.Column("confidence_level", sa.String(length=40), nullable=False),
        sa.Column("severity", sa.String(length=40), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("payload_json", sa.Text(), nullable=False),
        sa.Column("target_artifact_id", sa.String(length=36), nullable=True),
        sa.Column("target_artifact_version_id", sa.String(length=36), nullable=True),
        sa.Column("target_decision_id", sa.String(length=36), nullable=True),
        sa.Column("target_creative_input_id", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["author_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.ForeignKeyConstraint(["target_artifact_id"], ["artifacts.id"]),
        sa.ForeignKeyConstraint(["target_artifact_version_id"], ["artifact_versions.id"]),
        sa.ForeignKeyConstraint(["target_creative_input_id"], ["creative_inputs.id"]),
        sa.ForeignKeyConstraint(["target_decision_id"], ["decisions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_blackboard_entries_author_user_id"),
        "blackboard_entries",
        ["author_user_id"],
    )
    op.create_index(
        op.f("ix_blackboard_entries_entry_type"), "blackboard_entries", ["entry_type"]
    )
    op.create_index(op.f("ix_blackboard_entries_project_id"), "blackboard_entries", ["project_id"])
    op.create_index(op.f("ix_blackboard_entries_status"), "blackboard_entries", ["status"])
    op.create_index(
        op.f("ix_blackboard_entries_target_artifact_id"),
        "blackboard_entries",
        ["target_artifact_id"],
    )
    op.create_index(
        op.f("ix_blackboard_entries_target_artifact_version_id"),
        "blackboard_entries",
        ["target_artifact_version_id"],
    )
    op.create_index(
        op.f("ix_blackboard_entries_target_creative_input_id"),
        "blackboard_entries",
        ["target_creative_input_id"],
    )
    op.create_index(
        op.f("ix_blackboard_entries_target_decision_id"),
        "blackboard_entries",
        ["target_decision_id"],
    )

    op.create_table(
        "deliberation_records",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("created_by_user_id", sa.String(length=36), nullable=False),
        sa.Column("phase", sa.String(length=80), nullable=False),
        sa.Column("question", sa.Text(), nullable=False),
        sa.Column("recommended_next_action", sa.Text(), nullable=False),
        sa.Column("rationale", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("priority_inputs_json", sa.Text(), nullable=False),
        sa.Column("linked_entry_ids_json", sa.Text(), nullable=False),
        sa.Column("result_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_deliberation_records_created_by_user_id"),
        "deliberation_records",
        ["created_by_user_id"],
    )
    op.create_index(
        op.f("ix_deliberation_records_phase"), "deliberation_records", ["phase"]
    )
    op.create_index(
        op.f("ix_deliberation_records_project_id"),
        "deliberation_records",
        ["project_id"],
    )
    op.create_index(
        op.f("ix_deliberation_records_status"), "deliberation_records", ["status"]
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_deliberation_records_status"), table_name="deliberation_records")
    op.drop_index(op.f("ix_deliberation_records_project_id"), table_name="deliberation_records")
    op.drop_index(op.f("ix_deliberation_records_phase"), table_name="deliberation_records")
    op.drop_index(
        op.f("ix_deliberation_records_created_by_user_id"),
        table_name="deliberation_records",
    )
    op.drop_table("deliberation_records")

    op.drop_index(op.f("ix_blackboard_entries_target_decision_id"), table_name="blackboard_entries")
    op.drop_index(
        op.f("ix_blackboard_entries_target_creative_input_id"),
        table_name="blackboard_entries",
    )
    op.drop_index(
        op.f("ix_blackboard_entries_target_artifact_version_id"),
        table_name="blackboard_entries",
    )
    op.drop_index(
        op.f("ix_blackboard_entries_target_artifact_id"), table_name="blackboard_entries"
    )
    op.drop_index(op.f("ix_blackboard_entries_status"), table_name="blackboard_entries")
    op.drop_index(op.f("ix_blackboard_entries_project_id"), table_name="blackboard_entries")
    op.drop_index(op.f("ix_blackboard_entries_entry_type"), table_name="blackboard_entries")
    op.drop_index(op.f("ix_blackboard_entries_author_user_id"), table_name="blackboard_entries")
    op.drop_table("blackboard_entries")
