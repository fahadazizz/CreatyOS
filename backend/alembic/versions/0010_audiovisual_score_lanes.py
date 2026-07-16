"""audiovisual score lanes

Revision ID: 0010_audiovisual_score_lanes
Revises: 0009_audiovisual_score_foundation
Create Date: 2026-07-16
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0010_audiovisual_score_lanes"
down_revision: str | None = "0009_audiovisual_score_foundation"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "audiovisual_score_lane_entries",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("branch_id", sa.String(length=36), nullable=False),
        sa.Column("score_event_id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("created_by_user_id", sa.String(length=36), nullable=False),
        sa.Column("lane_type", sa.String(length=80), nullable=False),
        sa.Column("title", sa.String(length=240), nullable=False),
        sa.Column("intent", sa.Text(), nullable=False),
        sa.Column("content_json", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("linked_artifact_version_id", sa.String(length=36), nullable=True),
        sa.Column("linked_decision_id", sa.String(length=36), nullable=True),
        sa.Column("linked_blackboard_entry_id", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "lane_type IN ('audience_state','story_argument','image','performance_voice','graphics','sound_music','rhythm','evidence','production_state','review_notes')",
            name="ck_audiovisual_score_lane_entries_lane_type",
        ),
        sa.CheckConstraint(
            "status IN ('planned','needs_proof','approved','superseded')",
            name="ck_audiovisual_score_lane_entries_status",
        ),
        sa.ForeignKeyConstraint(["branch_id"], ["audiovisual_score_branches.id"]),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["linked_artifact_version_id"], ["artifact_versions.id"]),
        sa.ForeignKeyConstraint(["linked_blackboard_entry_id"], ["blackboard_entries.id"]),
        sa.ForeignKeyConstraint(["linked_decision_id"], ["decisions.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.ForeignKeyConstraint(["score_event_id"], ["audiovisual_score_events.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    for column in (
        "branch_id",
        "created_by_user_id",
        "lane_type",
        "linked_artifact_version_id",
        "linked_blackboard_entry_id",
        "linked_decision_id",
        "project_id",
        "score_event_id",
        "status",
    ):
        op.create_index(
            op.f(f"ix_audiovisual_score_lane_entries_{column}"),
            "audiovisual_score_lane_entries",
            [column],
            unique=False,
        )


def downgrade() -> None:
    for column in (
        "status",
        "score_event_id",
        "project_id",
        "linked_decision_id",
        "linked_blackboard_entry_id",
        "linked_artifact_version_id",
        "lane_type",
        "created_by_user_id",
        "branch_id",
    ):
        op.drop_index(
            op.f(f"ix_audiovisual_score_lane_entries_{column}"),
            table_name="audiovisual_score_lane_entries",
        )
    op.drop_table("audiovisual_score_lane_entries")
