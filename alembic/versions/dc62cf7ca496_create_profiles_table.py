"""Create profiles table

Revision ID: dc62cf7ca496
Revises: d1ebffa47328
Create Date: 2025-07-02 18:50:17.658973

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dc62cf7ca496'
down_revision: Union[str, Sequence[str], None] = 'd1ebffa47328'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profiles',
    sa.Column('first_name', sa.String(length=44), nullable=True),
    sa.Column('last_name', sa.String(length=44), nullable=True),
    sa.Column('bio', sa.String(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('profiles')
    # ### end Alembic commands ###
