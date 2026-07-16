"""creative inputs

Revision ID: 0004_creative_inputs
Revises: 0003_decision_log
Create Date: 2026-07-16
"""

from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0004_creative_inputs"
down_revision: str | None = "0003_decision_log"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "creative_inputs",
        sa.Column("id", sa.String(length=36), nullable=False),
        sa.Column("project_id", sa.String(length=36), nullable=False),
        sa.Column("production_id", sa.String(length=36), nullable=True),
        sa.Column("piece_id", sa.String(length=36), nullable=True),
        sa.Column("submitted_by_user_id", sa.String(length=36), nullable=False),
        sa.Column("input_type", sa.String(length=80), nullable=False),
        sa.Column("title", sa.String(length=240), nullable=False),
        sa.Column("source_label", sa.String(length=240), nullable=True),
        sa.Column("candidate_state", sa.String(length=40), nullable=False),
        sa.Column("body_json", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(["piece_id"], ["pieces.id"]),
        sa.ForeignKeyConstraint(["production_id"], ["productions.id"]),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.ForeignKeyConstraint(["submitted_by_user_id"], ["users.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_creative_inputs_input_type"), "creative_inputs", ["input_type"])
    op.create_index(op.f("ix_creative_inputs_piece_id"), "creative_inputs", ["piece_id"])
    op.create_index(
        op.f("ix_creative_inputs_production_id"), "creative_inputs", ["production_id"]
    )
    op.create_index(op.f("ix_creative_inputs_project_id"), "creative_inputs", ["project_id"])
    op.create_index(
        op.f("ix_creative_inputs_submitted_by_user_id"),
        "creative_inputs",
        ["submitted_by_user_id"],
    )


def downgrade() -> None:
    op.drop_index(op.f("ix_creative_inputs_submitted_by_user_id"), table_name="creative_inputs")
    op.drop_index(op.f("ix_creative_inputs_project_id"), table_name="creative_inputs")
    op.drop_index(op.f("ix_creative_inputs_production_id"), table_name="creative_inputs")
    op.drop_index(op.f("ix_creative_inputs_piece_id"), table_name="creative_inputs")
    op.drop_index(op.f("ix_creative_inputs_input_type"), table_name="creative_inputs")
    op.drop_table("creative_inputs")
