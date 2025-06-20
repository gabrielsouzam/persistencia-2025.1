"""fix appointment relationship with doctor

Revision ID: ed74d55f8d61
Revises: f53335e94b08
Create Date: 2025-06-12 13:32:10.627636

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ed74d55f8d61'
down_revision: Union[str, None] = 'f53335e94b08'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('appointment', 'doctor_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('appointment', 'doctor_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
