"""Add document processing fields

Revision ID: add_document_processing_fields
Revises: add_documents_table
Create Date: 2026-07-10
"""
from alembic import op
import sqlalchemy as sa

revision = "add_document_processing_fields"
down_revision = "add_documents"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("documents", sa.Column("page_count", sa.Integer(), nullable=True))
    op.add_column("documents", sa.Column("word_count", sa.Integer(), nullable=True))
    op.add_column("documents", sa.Column("character_count", sa.Integer(), nullable=True))
    op.add_column("documents", sa.Column("extracted_text", sa.Text(), nullable=True))
    op.add_column("documents", sa.Column("processed_at", sa.DateTime(timezone=True), nullable=True))


def downgrade() -> None:
    op.drop_column("documents", "processed_at")
    op.drop_column("documents", "extracted_text")
    op.drop_column("documents", "character_count")
    op.drop_column("documents", "word_count")
    op.drop_column("documents", "page_count")
