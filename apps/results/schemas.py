from marshmallow import Schema, pre_load, post_load, validates, validates_schema, ValidationError
from marshmallow.fields import Str, Int, DateTime, List, Nested, Boolean

from apps.extensions.messages import MSG_FIELD_REQUIRED


class ResultSchema(Schema):
    id = Str(required=True)
    job_id = Str(required=True)
    atividade_principal = Str(required=True)
    cnpj = Str(required=True)
    bairro = Str(required=True)
    cep = Str(required=True)
    complemento = Str(required=True)
    data_abertura = Str(required=True)
    data_pesquisa = Str(required=True)
    email = Str(required=True)
    hora_pesquisa = Str(required=True)
    logradouro = Str(required=True)
    matriz_filial = Str(required=True)
    municipio = Str(required=True)
    natureza_juridica = Str(required=True)
    nome_empresarial = Str(required=True)
    nome_fantasia = Str(required=True)
    numero = Str(required=True)
    porte = Str(required=True)
    telefone = Str(required=True)
    uf = Str(required=True)
    source = Str(required=True)
    creator_id = Str(required=True)
    creator_email = Str(required=True)
