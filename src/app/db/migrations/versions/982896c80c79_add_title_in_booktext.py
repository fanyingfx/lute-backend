# type: ignore
"""add title in bookText

Revision ID: 982896c80c79
Revises: 98c1180a7836
Create Date: 2024-02-27 14:33:31.800371

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
revision = "982896c80c79"
down_revision = "98c1180a7836"
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
    with op.batch_alter_table("booktexts", schema=None) as batch_op:
        batch_op.add_column(sa.Column("title", sa.String(length=300), nullable=True))

    with op.batch_alter_table("languages", schema=None) as batch_op:
        batch_op.alter_column("parser_name", existing_type=sa.VARCHAR(length=40), nullable=False)

    # ### end Alembic commands ###


def schema_downgrades() -> None:
    """schema downgrade migrations go here."""
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("languages", schema=None) as batch_op:
        batch_op.alter_column("parser_name", existing_type=sa.VARCHAR(length=40), nullable=True)

    with op.batch_alter_table("booktexts", schema=None) as batch_op:
        batch_op.drop_column("title")

    # ### end Alembic commands ###


def data_upgrades() -> None:
    """Add any optional data upgrade migrations here!"""


def data_downgrades() -> None:
    """Add any optional data downgrade migrations here!"""