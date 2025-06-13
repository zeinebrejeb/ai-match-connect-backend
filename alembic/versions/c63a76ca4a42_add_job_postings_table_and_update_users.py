"""add_job_postings_table_and_update_users

Revision ID: c63a76ca4a42
Revises: 16425a31ccab
Create Date: 2025-06-05 12:42:10.746725

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c63a76ca4a42'
down_revision: Union[str, None] = '16425a31ccab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
