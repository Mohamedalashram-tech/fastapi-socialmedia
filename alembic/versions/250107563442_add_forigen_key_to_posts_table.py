"""add forigen-key to posts table

Revision ID: 250107563442
Revises: 0f20e3db871b
Create Date: 2026-02-12 01:18:24.310887

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '250107563442'
down_revision: Union[str, Sequence[str], None] = '0f20e3db871b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("posts", sa.Column("owner_id" , sa.Integer() , nullable= False))
    op.create_foreign_key("post_user_fk" , source_table="posts" , referent_table="users" , local_cols=["owner_id"] , remote_cols=["id"] , ondelete= "CASCADE")
    pass


def downgrade() -> None:
    op.drop_column("posts" , "owner_id")
    op.drop_constraint("post_user_fk" , table_name="posts")
    pass
