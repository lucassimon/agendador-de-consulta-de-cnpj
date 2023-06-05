from enum import StrEnum
from apps.extensions.db import db
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.sql import func


class Result(db.Model):
    __tablename__ = 'result'

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('job.id'), nullable=False)
    job = db.relationship("Job", backref="jobs", cascade="all,delete",)

    atividade_principal = db.Column(db.String(), nullable=False)
    cnpj = db.Column(db.String(), nullable=False)
    bairro = db.Column(db.String(), nullable=False)
    cep = db.Column(db.String(), nullable=False)
    complemento = db.Column(db.String(), nullable=False)
    data_abertura = db.Column(db.String(), nullable=False)
    data_pesquisa = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    hora_pesquisa = db.Column(db.String(), nullable=False)
    logradouro = db.Column(db.String(), nullable=False)
    matriz_filial = db.Column(db.String(), nullable=False)
    municipio = db.Column(db.String(), nullable=False)
    natureza_juridica = db.Column(db.String(), nullable=False)
    nome_empresarial = db.Column(db.String(), nullable=False)
    nome_fantasia = db.Column(db.String(), nullable=False)
    numero = db.Column(db.String(), nullable=False)
    porte = db.Column(db.String(), nullable=False)
    telefone = db.Column(db.String(), nullable=False)
    uf = db.Column(db.String(), nullable=False)

    source = db.Column(db.String(), nullable=False)

    creator_id = db.Column(db.String(), nullable=False)
    creator_email = db.Column(db.String(), nullable=False)
    created = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated = db.Column(db.DateTime(timezone=True), onupdate=func.now())
