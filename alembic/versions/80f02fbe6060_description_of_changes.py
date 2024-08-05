"""description of changes

Revision ID: 80f02fbe6060
Revises: b0bc2be30cfa
Create Date: 2024-08-05 15:27:28.001097

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80f02fbe6060'
down_revision: Union[str, None] = 'b0bc2be30cfa'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
