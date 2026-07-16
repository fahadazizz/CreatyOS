"""audiovisual score event relationships

Revision ID: 0011_audiovisual_score_event_relationships
Revises: 0010_audiovisual_score_lanes
Create Date: 2026-07-16
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0011_audiovisual_score_event_relationships"
down_revision: str | None = "0010_audiovisual_score_lanes"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "audiovisual_score_event_relationships",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("branch_id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("created_by_user_id", sa.String(length=36), nullable=False),
        sa.Column("from_event_id", sa.String(length=36), nullable=False),
        sa.Column("to_event_id", sa.String(length=36), nullable=False),
        sa.Column("relationship_type", sa.String(length=80), nullable=False),
        sa.Column("title", sa.String(length=240), nullable=False),
        sa.Column("rationale", sa.Text(), nullable=False),
        sa.Column("expected_viewer_effect", sa.Text(), nullable=False),
        sa.Column("timing_logic", sa.Text(), nullable=False),
        sa.Column("continuity_impact", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("linked_artifact_version_id", sa.String(length=36), nullable=True),
        sa.Column("linked_decision_id", sa.String(length=36), nullable=True),
        sa.Column("linked_blackboard_entry_id", sa.String(length=36), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.CheckConstraint(
            "relationship_type IN ('reveal','contrast','continuation','interruption','escalation','compression','reaction','pause','payoff','transition','misdirection','evidence_support')",
            name="ck_audiovisual_score_event_relationships_type",
        ),
        sa.CheckConstraint(
            "status IN ('planned','needs_proof','approved','superseded')",
            name="ck_audiovisual_score_event_relationships_status",
        ),
        sa.CheckConstraint(
            "from_event_id != to_event_id",
            name="ck_audiovisual_score_event_relationships_not_self",
        ),
        sa.ForeignKeyConstraint(["branch_id"], ["audiovisual_score_branches.id"]),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["from_event_id"], ["audiovisual_score_events.id"]),
        sa.ForeignKeyConstraint(["linked_artifact_version_id"], ["artifact_versions.id"]),
        sa.ForeignKeyConstraint(["linked_blackboard_entry_id"], ["blackboard_entries.id"]),
        sa.ForeignKeyConstraint(["linked_decision_id"], ["decisions.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.ForeignKeyConstraint(["to_event_id"], ["audiovisual_score_events.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    for column in (
        "branch_id",
        "created_by_user_id",
        "from_event_id",
        "linked_artifact_version_id",
        "linked_blackboard_entry_id",
        "linked_decision_id",
        "project_id",
        "relationship_type",
        "status",
        "to_event_id",
    ):
        op.create_index(
            op.f(f"ix_audiovisual_score_event_relationships_{column}"),
            "audiovisual_score_event_relationships",
            [column],
            unique=False,
        )


def downgrade() -> None:
    for column in (
        "to_event_id",
        "status",
        "relationship_type",
        "project_id",
        "linked_decision_id",
        "linked_blackboard_entry_id",
        "linked_artifact_version_id",
        "from_event_id",
        "created_by_user_id",
        "branch_id",
    ):
        op.drop_index(
            op.f(f"ix_audiovisual_score_event_relationships_{column}"),
            table_name="audiovisual_score_event_relationships",
        )
    op.drop_table("audiovisual_score_event_relationships")
