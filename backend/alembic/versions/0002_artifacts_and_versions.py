"""artifacts and versions

Revision ID: 0002_artifacts_and_versions
Revises: 0001_foundation_project_hierarchy
Create Date: 2026-07-16
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002_artifacts_and_versions"
down_revision: str | None = "0001_foundation_project_hierarchy"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "artifacts",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("production_id", sa.String(length=36), nullable=True),
        sa.Column("piece_id", sa.String(length=36), nullable=True),
        sa.Column("owner_user_id", sa.String(length=36), nullable=False),
        sa.Column("artifact_type", sa.String(length=80), nullable=False),
        sa.Column("title", sa.String(length=240), nullable=False),
        sa.Column("status", sa.String(length=40), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["owner_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["piece_id"], ["pieces.id"]),
        sa.ForeignKeyConstraint(["production_id"], ["productions.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_artifacts_artifact_type"), "artifacts", ["artifact_type"])
    op.create_index(op.f("ix_artifacts_owner_user_id"), "artifacts", ["owner_user_id"])
    op.create_index(op.f("ix_artifacts_piece_id"), "artifacts", ["piece_id"])
    op.create_index(op.f("ix_artifacts_production_id"), "artifacts", ["production_id"])
    op.create_index(op.f("ix_artifacts_project_id"), "artifacts", ["project_id"])

    op.create_table(
        "artifact_versions",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("artifact_id", sa.String(length=36), nullable=False),
        sa.Column("version_number", sa.Integer(), nullable=False),
        sa.Column("schema_version", sa.String(length=40), nullable=False),
        sa.Column("author_user_id", sa.String(length=36), nullable=False),
        sa.Column("parent_version_id", sa.String(length=36), nullable=True),
        sa.Column("confidence_level", sa.String(length=40), nullable=False),
        sa.Column("body_json", sa.Text(), nullable=False),
        sa.Column("linked_decisions_json", sa.Text(), nullable=False),
        sa.Column("linked_evidence_json", sa.Text(), nullable=False),
        sa.Column("open_questions_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["artifact_id"], ["artifacts.id"]),
        sa.ForeignKeyConstraint(["author_user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["parent_version_id"], ["artifact_versions.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("artifact_id", "version_number", name="uq_artifact_versions_number"),
    )
    op.create_index(op.f("ix_artifact_versions_artifact_id"), "artifact_versions", ["artifact_id"])
    op.create_index(
        op.f("ix_artifact_versions_author_user_id"), "artifact_versions", ["author_user_id"]
    )
    op.create_index(
        op.f("ix_artifact_versions_parent_version_id"),
        "artifact_versions",
        ["parent_version_id"],
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_artifact_versions_parent_version_id"), table_name="artifact_versions")
    op.drop_index(op.f("ix_artifact_versions_author_user_id"), table_name="artifact_versions")
    op.drop_index(op.f("ix_artifact_versions_artifact_id"), table_name="artifact_versions")
    op.drop_table("artifact_versions")
    op.drop_index(op.f("ix_artifacts_project_id"), table_name="artifacts")
    op.drop_index(op.f("ix_artifacts_production_id"), table_name="artifacts")
    op.drop_index(op.f("ix_artifacts_piece_id"), table_name="artifacts")
    op.drop_index(op.f("ix_artifacts_owner_user_id"), table_name="artifacts")
    op.drop_index(op.f("ix_artifacts_artifact_type"), table_name="artifacts")
    op.drop_table("artifacts")
