"""create result table

Revision ID: 57bb61e5085e
Revises: d8ad5dfa606b
Create Date: 2023-06-01 22:52:11.873704

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '57bb61e5085e'
down_revision = 'd8ad5dfa606b'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'result',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('job_id', sa.Integer, nullable=False),
        sa.Column('atividade_principal', sa.String, nullable=False),
        sa.Column('cnpj', sa.String, nullable=False),
        sa.Column('bairro', sa.String, nullable=False),
        sa.Column('cep', sa.String, nullable=False),
        sa.Column('complemento', sa.String, nullable=False),
        sa.Column('data_abertura', sa.String, nullable=False),
        sa.Column('data_pesquisa', sa.String, nullable=False),
        sa.Column('email', sa.String, nullable=False),
        sa.Column('hora_pesquisa', sa.String, nullable=False),
        sa.Column('logradouro', sa.String, nullable=False),
        sa.Column('matriz_filial', sa.String, nullable=False),
        sa.Column('municipio', sa.String, nullable=False),
        sa.Column('natureza_juridica', sa.String, nullable=False),
        sa.Column('nome_empresarial', sa.String, nullable=False),
        sa.Column('nome_fantasia', sa.String, nullable=False),
        sa.Column('numero', sa.String, nullable=False),
        sa.Column('porte', sa.String, nullable=False),
        sa.Column('telefone', sa.String, nullable=False),
        sa.Column('uf', sa.String, nullable=False),

        sa.Column('source', sa.String, nullable=False),

        sa.Column('creator_id', sa.String, nullable=False),
        sa.Column('creator_email', sa.String, nullable=False),
        sa.Column('created', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('updated', sa.DateTime(timezone=True), onupdate=sa.func.now()),
    )

    op.create_foreign_key(
        'job_result_fk',
        source_table="result",
        referent_table="job",
        local_cols=['job_id'], remote_cols=['id'], ondelete="CASCADE"
    )


def downgrade():
    op.drop_constraint('job_result_fk', table_name="result")
    op.drop_table('result')
