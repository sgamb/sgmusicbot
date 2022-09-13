"""rename record_collection table

Revision ID: 9e52b070a882
Revises: 
Create Date: 2022-07-21 13:50:50.524824

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9e52b070a882'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.rename_table(
        'record_collection',
        'records',
    )


def downgrade() -> None:
    op.rename_table(
        'records',
        'record_collection',
    )
