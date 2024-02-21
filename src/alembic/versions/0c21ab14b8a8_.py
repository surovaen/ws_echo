"""empty message

Revision ID: 0c21ab14b8a8
Revises: 
Create Date: 2024-02-10 19:37:39.572371

"""
from typing import Sequence, Union

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op


# revision identifiers, used by Alembic.
revision: str = '0c21ab14b8a8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('user',
                    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
                    sa.Column('username', sa.String(), unique=True, nullable=False),
                    sa.Column('password', sa.String(), nullable=True),
                    sa.Column('token', sa.String(), nullable=True),
                    )
    op.create_index(op.f('ix_user_id'), 'user', ['id'], unique=True)

    op.create_table('history',
                    sa.Column('id', sa.Integer(), primary_key=True, autoincrement=True),
                    sa.Column('username', sa.String(), unique=True, nullable=False),
                    sa.Column('records', postgresql.JSON(astext_type=sa.Text()), nullable=False),
                    )
    op.create_index(op.f('ix_history_id'), 'history', ['id'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_user_id'), table_name='user')
    op.drop_table('user')

    op.drop_index(op.f('ix_history_id'), table_name='history')
    op.drop_table('history')
