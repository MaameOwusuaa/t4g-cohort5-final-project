"""create categories table

Revision ID: d09bb46ba43e
Revises: da044f1de6de
Create Date: 2026-08-06 20:51:59.184899

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'd09bb46ba43e'
down_revision: Union[str, Sequence[str], None] = 'da044f1de6de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

    
def upgrade() -> None:
    op.create_table(
        'categories',
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(
        op.f('ix_categories_id'),
        'categories',
        ['id'],
        unique=False
    )