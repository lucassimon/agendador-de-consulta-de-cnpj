"""create job table


Revision ID: d8ad5dfa606b
Revises:
Create Date: 2023-05-31 17:37:04.136033

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8ad5dfa606b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'jobs',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('title', sa.String, nullable=False),
        sa.Column('description', sa.Text, nullable=False),
        sa.Column('cpf_cnpj', sa.String, nullable=False),
        sa.Column('status', sa.String, nullable=False),
        sa.Column('priority', sa.Integer, nullable=False),
        sa.Column('duration', sa.Integer, nullable=False),
        sa.Column('date', sa.DateTime(timezone=True), nullable=False),
        sa.Column('creator_id', sa.String, nullable=False),
        sa.Column('creator_email', sa.String, nullable=False),
        sa.Column('created', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated', sa.DateTime(timezone=True), onupdate=sa.func.now())
    )


def downgrade():
    op.drop_table('jobs')
