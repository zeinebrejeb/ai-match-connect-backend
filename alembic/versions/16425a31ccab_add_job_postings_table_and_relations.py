"""add_job_postings_table_and_relations

Revision ID: 16425a31ccab
Revises: 7678b2b43b95
Create Date: 2025-06-01 22:24:10.867767

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '16425a31ccab'
down_revision: Union[str, None] = '7678b2b43b95'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
