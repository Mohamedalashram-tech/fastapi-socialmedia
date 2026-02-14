"""create users table

Revision ID: 0f20e3db871b
Revises: 9e5b6e5cb587
Create Date: 2026-02-10 20:21:24.732019

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0f20e3db871b'
down_revision: Union[str, Sequence[str], None] = '9e5b6e5cb587'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("users" 
                    , sa.Column("id" , sa.Integer() , nullable = False , )
                    , sa.Column("email" , sa.String() , nullable = False )
                    , sa.Column("password" , sa.String() , nullable = False)
                    , sa.Column("created_at" , sa.TIMESTAMP(timezone= True),server_default = sa.text("now()") , nullable = False)
                    , sa.PrimaryKeyConstraint("id")
                    , sa.UniqueConstraint("email")
                    )
    
    pass


def downgrade() -> None:
    op.drop_table("users")
    pass
