"""create posts table

Revision ID: c7f99977afe2
Revises: 
Create Date: 2026-02-10 19:11:57.424080

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c7f99977afe2'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table("posts" 
                    , sa.Column("id" , sa.Integer() , nullable = False , primary_key= True)
                    , sa.Column("title" , sa.String() , nullable = False )
                    , sa.Column("content" , sa.String() , nullable = False)
                    , sa.Column("activaties" , sa.String() , nullable = True)
                    )
    pass


def downgrade():
    op.drop_table("posts")
    
    pass
