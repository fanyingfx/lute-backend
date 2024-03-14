# type: ignore
"""add unique constrainst on word_images word_id

Revision ID: a24f66bcae0a
Revises: 18cd8bf35835
Create Date: 2024-03-12 17:42:34.177080

"""
from __future__ import annotations

import warnings

import sqlalchemy as sa
from advanced_alchemy.types import GUID, ORA_JSONB, DateTimeUTC, EncryptedString, EncryptedText
from alembic import op
from sqlalchemy import Text  # noqa: F401

__all__ = ["downgrade", "upgrade", "schema_upgrades", "schema_downgrades", "data_upgrades", "data_downgrades"]

sa.GUID = GUID
sa.DateTimeUTC = DateTimeUTC
sa.ORA_JSONB = ORA_JSONB
sa.EncryptedString = EncryptedString
sa.EncryptedText = EncryptedText

# revision identifiers, used by Alembic.
revision = "a24f66bcae0a"
down_revision = "18cd8bf35835"
branch_labels = None
depends_on = None


def upgrade() -> None:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        with op.get_context().autocommit_block():
            schema_upgrades()
            data_upgrades()


def downgrade() -> None:
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore", category=UserWarning)
        with op.get_context().autocommit_block():
            data_downgrades()
            schema_downgrades()


def schema_upgrades() -> None:
    """schema upgrade migrations go here."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("word_images", schema=None) as batch_op:
        batch_op.create_unique_constraint(batch_op.f("uq_word_images_word_id"), ["word_id"])

    with op.batch_alter_table("words", schema=None) as batch_op:
        batch_op.alter_column("first_word", existing_type=sa.VARCHAR(length=100), nullable=False)

    # ### end Alembic commands ###


def schema_downgrades() -> None:
    """schema downgrade migrations go here."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("words", schema=None) as batch_op:
        batch_op.alter_column("first_word", existing_type=sa.VARCHAR(length=100), nullable=True)

    with op.batch_alter_table("word_images", schema=None) as batch_op:
        batch_op.drop_constraint(batch_op.f("uq_word_images_word_id"), type_="unique")

    # ### end Alembic commands ###


def data_upgrades() -> None:
    """Add any optional data upgrade migrations here!"""


def data_downgrades() -> None:
    """Add any optional data downgrade migrations here!"""