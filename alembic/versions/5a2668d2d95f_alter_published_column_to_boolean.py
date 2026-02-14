"""alter published column to boolean

Revision ID: 5a2668d2d95f
Revises: 5e6f411187a9
Create Date: 2026-02-12 04:06:49.083218

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a2668d2d95f'
down_revision: Union[str, Sequence[str], None] = '5e6f411187a9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # تعديل عمود published ليكون Boolean
    op.alter_column('posts', 'published',
               existing_type=sa.VARCHAR(), # النوع القديم (في الـ DB)
               type_=sa.Boolean(),         # النوع الجديد اللي عايزينه
               nullable=True,              # عشان مش نضمن إن كل الداتا القديمة تمشي مع الـ Boolean
               postgresql_using='published::boolean' # ده السحر اللي بيحول النص لـ Boolean في Postgres
               )

def downgrade() -> None:
    # عكس العملية: رجع العمود نص تاني لو حبيت تـ downgrade
    op.alter_column('posts', 'published',
               existing_type=sa.Boolean(),
               type_=sa.VARCHAR(),
               nullable=True)