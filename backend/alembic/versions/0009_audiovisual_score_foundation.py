"""audiovisual score foundation

Revision ID: 0009_audiovisual_score_foundation
Revises: 0008_milestone_2_state_constraints
Create Date: 2026-07-16
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0009_audiovisual_score_foundation"
down_revision: str | None = "0008_milestone_2_state_constraints"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "audiovisual_score_branches",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("created_by_user_id", sa.String(length=36), nullable=False),
        sa.Column("name", sa.String(length=240), nullable=False),
        sa.Column("purpose", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("source_artifact_version_id", sa.String(length=36), nullable=True),
        sa.Column("source_decision_id", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "status IN ('draft','active','superseded')",
            name="ck_audiovisual_score_branches_status",
        ),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.ForeignKeyConstraint(["source_artifact_version_id"], ["artifact_versions.id"]),
        sa.ForeignKeyConstraint(["source_decision_id"], ["decisions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_audiovisual_score_branches_created_by_user_id"),
        "audiovisual_score_branches",
        ["created_by_user_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_audiovisual_score_branches_project_id"),
        "audiovisual_score_branches",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_audiovisual_score_branches_source_artifact_version_id"),
        "audiovisual_score_branches",
        ["source_artifact_version_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_audiovisual_score_branches_source_decision_id"),
        "audiovisual_score_branches",
        ["source_decision_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_audiovisual_score_branches_status"),
        "audiovisual_score_branches",
        ["status"],
        unique=False,
    )

    op.create_table(
        "audiovisual_score_events",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("branch_id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("created_by_user_id", sa.String(length=36), nullable=False),
        sa.Column("parent_event_id", sa.String(length=36), nullable=True),
        sa.Column("hierarchy_level", sa.String(length=80), nullable=False),
        sa.Column("title", sa.String(length=240), nullable=False),
        sa.Column("sort_key", sa.String(length=120), nullable=False),
        sa.Column("why", sa.Text(), nullable=False),
        sa.Column("what", sa.Text(), nullable=False),
        sa.Column("how", sa.Text(), nullable=False),
        sa.Column("where_when_json", sa.Text(), nullable=False),
        sa.Column("duration_policy", sa.String(length=40), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("linked_artifact_version_id", sa.String(length=36), nullable=True),
        sa.Column("linked_decision_id", sa.String(length=36), nullable=True),
        sa.Column("linked_blackboard_entry_id", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "hierarchy_level IN ('piece','act','sequence','scene','beat','shot','event','cut')",
            name="ck_audiovisual_score_events_hierarchy_level",
        ),
        sa.CheckConstraint(
            "duration_policy IN ('elastic','fixed','relative')",
            name="ck_audiovisual_score_events_duration_policy",
        ),
        sa.CheckConstraint(
            "status IN ('planned','needs_proof','approved','superseded')",
            name="ck_audiovisual_score_events_status",
        ),
        sa.ForeignKeyConstraint(["branch_id"], ["audiovisual_score_branches.id"]),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["linked_artifact_version_id"], ["artifact_versions.id"]),
        sa.ForeignKeyConstraint(["linked_blackboard_entry_id"], ["blackboard_entries.id"]),
        sa.ForeignKeyConstraint(["linked_decision_id"], ["decisions.id"]),
        sa.ForeignKeyConstraint(["parent_event_id"], ["audiovisual_score_events.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    for column in (
        "branch_id",
        "created_by_user_id",
        "hierarchy_level",
        "linked_artifact_version_id",
        "linked_blackboard_entry_id",
        "linked_decision_id",
        "parent_event_id",
        "project_id",
        "sort_key",
        "status",
    ):
        op.create_index(
            op.f(f"ix_audiovisual_score_events_{column}"),
            "audiovisual_score_events",
            [column],
            unique=False,
        )


def downgrade() -> None:
    for column in (
        "status",
        "sort_key",
        "project_id",
        "parent_event_id",
        "linked_decision_id",
        "linked_blackboard_entry_id",
        "linked_artifact_version_id",
        "hierarchy_level",
        "created_by_user_id",
        "branch_id",
    ):
        op.drop_index(
            op.f(f"ix_audiovisual_score_events_{column}"),
            table_name="audiovisual_score_events",
        )
    op.drop_table("audiovisual_score_events")

    for column in (
        "status",
        "source_decision_id",
        "source_artifact_version_id",
        "project_id",
        "created_by_user_id",
    ):
        op.drop_index(
            op.f(f"ix_audiovisual_score_branches_{column}"),
            table_name="audiovisual_score_branches",
        )
    op.drop_table("audiovisual_score_branches")
