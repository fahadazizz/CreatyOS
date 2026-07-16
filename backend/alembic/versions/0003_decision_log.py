"""decision log

Revision ID: 0003_decision_log
Revises: 0002_artifacts_and_versions
Create Date: 2026-07-16
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0003_decision_log"
down_revision: str | None = "0002_artifacts_and_versions"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "decisions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("owner_user_id", sa.String(length=36), nullable=False),
        sa.Column("target_artifact_id", sa.String(length=36), nullable=True),
        sa.Column("target_artifact_version_id", sa.String(length=36), nullable=True),
        sa.Column("title", sa.String(length=240), nullable=False),
        sa.Column("decision_text", sa.Text(), nullable=False),
        sa.Column("selected_option", sa.String(length=500), nullable=False),
        sa.Column("rationale", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("alternatives_json", sa.Text(), nullable=False),
        sa.Column("evidence_json", sa.Text(), nullable=False),
        sa.Column("risks_json", sa.Text(), nullable=False),
        sa.Column("affected_scope_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["owner_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.ForeignKeyConstraint(["target_artifact_id"], ["artifacts.id"]),
        sa.ForeignKeyConstraint(["target_artifact_version_id"], ["artifact_versions.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_decisions_owner_user_id"), "decisions", ["owner_user_id"])
    op.create_index(op.f("ix_decisions_project_id"), "decisions", ["project_id"])
    op.create_index(op.f("ix_decisions_target_artifact_id"), "decisions", ["target_artifact_id"])
    op.create_index(
        op.f("ix_decisions_target_artifact_version_id"),
        "decisions",
        ["target_artifact_version_id"],
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_decisions_target_artifact_version_id"), table_name="decisions")
    op.drop_index(op.f("ix_decisions_target_artifact_id"), table_name="decisions")
    op.drop_index(op.f("ix_decisions_project_id"), table_name="decisions")
    op.drop_index(op.f("ix_decisions_owner_user_id"), table_name="decisions")
    op.drop_table("decisions")
