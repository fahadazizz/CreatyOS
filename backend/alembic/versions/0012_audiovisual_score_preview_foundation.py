"""audiovisual score preview foundation

Revision ID: 0012_audiovisual_score_preview_foundation
Revises: 0011_audiovisual_score_event_relationships
Create Date: 2026-07-16
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0012_audiovisual_score_preview_foundation"
down_revision: str | None = "0011_audiovisual_score_event_relationships"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "audiovisual_score_preview_prototypes",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("branch_id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("created_by_user_id", sa.String(length=36), nullable=False),
        sa.Column("prototype_type", sa.String(length=80), nullable=False),
        sa.Column("title", sa.String(length=240), nullable=False),
        sa.Column("purpose", sa.Text(), nullable=False),
        sa.Column("test_question", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("linked_decision_id", sa.String(length=36), nullable=True),
        sa.Column("linked_blackboard_entry_id", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "prototype_type IN ('cards','boards','animatic_stub','paper_edit')",
            name="ck_audiovisual_score_preview_prototypes_type",
        ),
        sa.CheckConstraint(
            "status IN ('draft','ready_for_screening','screened','superseded')",
            name="ck_audiovisual_score_preview_prototypes_status",
        ),
        sa.ForeignKeyConstraint(["branch_id"], ["audiovisual_score_branches.id"]),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["linked_blackboard_entry_id"], ["blackboard_entries.id"]),
        sa.ForeignKeyConstraint(["linked_decision_id"], ["decisions.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    for column in (
        "branch_id",
        "created_by_user_id",
        "linked_blackboard_entry_id",
        "linked_decision_id",
        "project_id",
        "prototype_type",
        "status",
    ):
        op.create_index(
            op.f(f"ix_audiovisual_score_preview_prototypes_{column}"),
            "audiovisual_score_preview_prototypes",
            [column],
            unique=False,
        )

    op.create_table(
        "audiovisual_score_preview_items",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("prototype_id", sa.String(length=36), nullable=False),
        sa.Column("branch_id", sa.String(length=36), nullable=False),
        sa.Column("score_event_id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("created_by_user_id", sa.String(length=36), nullable=False),
        sa.Column("item_type", sa.String(length=80), nullable=False),
        sa.Column("title", sa.String(length=240), nullable=False),
        sa.Column("sort_key", sa.String(length=120), nullable=False),
        sa.Column("test_focus", sa.Text(), nullable=False),
        sa.Column("inspection_notes", sa.Text(), nullable=False),
        sa.Column("score_event_why_snapshot", sa.Text(), nullable=False),
        sa.Column("body_json", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("linked_artifact_version_id", sa.String(length=36), nullable=True),
        sa.Column("linked_decision_id", sa.String(length=36), nullable=True),
        sa.Column("linked_blackboard_entry_id", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "item_type IN ('card','board','scratch_narration','temp_still','temp_clip','music_placeholder','timing','caption','rough_transition')",
            name="ck_audiovisual_score_preview_items_type",
        ),
        sa.CheckConstraint(
            "status IN ('planned','ready','needs_revision','superseded')",
            name="ck_audiovisual_score_preview_items_status",
        ),
        sa.ForeignKeyConstraint(["branch_id"], ["audiovisual_score_branches.id"]),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["linked_artifact_version_id"], ["artifact_versions.id"]),
        sa.ForeignKeyConstraint(["linked_blackboard_entry_id"], ["blackboard_entries.id"]),
        sa.ForeignKeyConstraint(["linked_decision_id"], ["decisions.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.ForeignKeyConstraint(["prototype_id"], ["audiovisual_score_preview_prototypes.id"]),
        sa.ForeignKeyConstraint(["score_event_id"], ["audiovisual_score_events.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    for column in (
        "branch_id",
        "created_by_user_id",
        "item_type",
        "linked_artifact_version_id",
        "linked_blackboard_entry_id",
        "linked_decision_id",
        "project_id",
        "prototype_id",
        "score_event_id",
        "sort_key",
        "status",
    ):
        op.create_index(
            op.f(f"ix_audiovisual_score_preview_items_{column}"),
            "audiovisual_score_preview_items",
            [column],
            unique=False,
        )


def downgrade() -> None:
    for column in (
        "status",
        "sort_key",
        "score_event_id",
        "prototype_id",
        "project_id",
        "linked_decision_id",
        "linked_blackboard_entry_id",
        "linked_artifact_version_id",
        "item_type",
        "created_by_user_id",
        "branch_id",
    ):
        op.drop_index(
            op.f(f"ix_audiovisual_score_preview_items_{column}"),
            table_name="audiovisual_score_preview_items",
        )
    op.drop_table("audiovisual_score_preview_items")

    for column in (
        "status",
        "prototype_type",
        "project_id",
        "linked_decision_id",
        "linked_blackboard_entry_id",
        "created_by_user_id",
        "branch_id",
    ):
        op.drop_index(
            op.f(f"ix_audiovisual_score_preview_prototypes_{column}"),
            table_name="audiovisual_score_preview_prototypes",
        )
    op.drop_table("audiovisual_score_preview_prototypes")
