# type: ignore
"""book -> books ,

Revision ID: 37aff0b14db9
Revises: 7294c8cb9991
Create Date: 2024-02-10 04:31:49.697820+00:00

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
revision = "37aff0b14db9"
down_revision = "7294c8cb9991"
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
    op.create_table(
        "books",
        sa.Column("id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False),
        sa.Column("book_name", sa.String(length=300), nullable=False),
        sa.Column("published_at", sa.Date(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(timezone=True), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False
        ),
        sa.Column(
            "updated_at", sa.DateTime(timezone=True), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_books")),
    )
    op.create_table(
        "booktexts",
        sa.Column("id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False),
        sa.Column("ref_book_id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False),
        sa.Column("book_text", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["ref_book_id"], ["books.id"], name=op.f("fk_booktexts_ref_book_id_books")),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_booktexts")),
    )
    op.create_table(
        "word_images",
        sa.Column("id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False),
        sa.Column("word_id", sa.BigInteger().with_variant(sa.Integer(), "sqlite"), nullable=False),
        sa.Column("word_image_name", sa.String(length=100), nullable=False),
        sa.Column("word_image_path", sa.String(length=100), nullable=False),
        sa.ForeignKeyConstraint(["word_id"], ["words.id"], name=op.f("fk_word_images_word_id_words")),
        sa.PrimaryKeyConstraint("word_id", "id", name=op.f("pk_word_images")),
    )
    op.drop_table("booktext")
    op.drop_table("book")
    # ### end Alembic commands ###


def schema_downgrades() -> None:
    """schema downgrade migrations go here."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "book",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("book_name", sa.VARCHAR(length=300), nullable=False),
        sa.Column("published_at", sa.DATE(), nullable=True),
        sa.Column("created_at", sa.DATETIME(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.Column("updated_at", sa.DATETIME(), server_default=sa.text("(CURRENT_TIMESTAMP)"), nullable=False),
        sa.PrimaryKeyConstraint("id", name="pk_book"),
    )
    op.create_table(
        "booktext",
        sa.Column("id", sa.INTEGER(), nullable=False),
        sa.Column("ref_book_id", sa.INTEGER(), nullable=False),
        sa.Column("book_text", sa.TEXT(), nullable=False),
        sa.ForeignKeyConstraint(["ref_book_id"], ["book.id"], name="fk_booktext_ref_book_id_book"),
        sa.PrimaryKeyConstraint("id", name="pk_booktext"),
    )
    op.drop_table("word_images")
    op.drop_table("booktexts")
    op.drop_table("books")
    # ### end Alembic commands ###


def data_upgrades() -> None:
    """Add any optional data upgrade migrations here!"""


def data_downgrades() -> None:
    """Add any optional data downgrade migrations here!"""