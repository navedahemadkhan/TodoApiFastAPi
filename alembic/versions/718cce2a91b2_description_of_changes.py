"""description of changes

Revision ID: 718cce2a91b2
Revises: 80f02fbe6060
Create Date: 2024-08-05 15:32:45.838356

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '718cce2a91b2'
down_revision: Union[str, None] = '80f02fbe6060'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
