"""rename_fisrt_name_to_first_name_in_candidate_profiles

Revision ID: d93bc9ef6c65
Revises: 1d18281debc1
Create Date: 2025-05-19 23:05:42.290309

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd93bc9ef6c65'
down_revision: Union[str, None] = '1d18281debc1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
