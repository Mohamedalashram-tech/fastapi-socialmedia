"""add two columns to posts table

Revision ID: 9e5b6e5cb587
Revises: c7f99977afe2
Create Date: 2026-02-10 19:35:18.283982

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e5b6e5cb587'
down_revision: Union[str, Sequence[str], None] = 'c7f99977afe2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    
    op.add_column("posts" , sa.Column("published" , sa.String() , nullable= False))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('now()')))
    
    pass


def downgrade() -> None:
    op.drop_column("posts" , "published")
    op.drop_column("posts" , "created_at")
    pass
