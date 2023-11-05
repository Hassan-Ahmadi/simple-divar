"""unique title from ads removed

Revision ID: 9a4492b1ea7b
Revises: c2775f54728a
Create Date: 2023-11-05 10:57:36.574267

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9a4492b1ea7b'
down_revision: Union[str, None] = 'c2775f54728a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_ads_title', table_name='ads')
    op.create_index(op.f('ix_ads_title'), 'ads', ['title'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_ads_title'), table_name='ads')
    op.create_index('ix_ads_title', 'ads', ['title'], unique=False)
    # ### end Alembic commands ###