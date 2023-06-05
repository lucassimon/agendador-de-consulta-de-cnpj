from marshmallow import Schema, pre_load, post_load, validates, validates_schema, ValidationError
from marshmallow.fields import Str, Int, DateTime, List, Nested, Boolean

from apps.extensions.messages import MSG_FIELD_REQUIRED

from .utils import Cpf


def check_cpf(data):
    return Cpf(data).validate()


class CreateJobInput(Schema):
    title = Str(required=True, error_messages={'required': MSG_FIELD_REQUIRED})
    description = Str(required=True, error_messages={'required': MSG_FIELD_REQUIRED})
    cpf_cnpj = Str(required=True, error_messages={'required': MSG_FIELD_REQUIRED})
    date = DateTime(required=True, error_messages={'required': MSG_FIELD_REQUIRED})
    priority = Int(default=0, error_messages={'required': MSG_FIELD_REQUIRED})
    status = Str(
        error_messages={'required': MSG_FIELD_REQUIRED},
        default='created'
    )

    def normalize_cpf_cnpj(self, value, **kwargs):
        # normalizo a string retirando caracteres especiais
        return value.strip().replace(".", "").replace("-", "").replace("/", "")

    @post_load
    def render_cpf_cnpj(self, payload, **kwargs):
        payload["cpf_cnpj"] = self.normalize_cpf_cnpj(payload["cpf_cnpj"])
        return payload

    @validates("cpf_cnpj")
    def validate_cpf_cnpj(self, value):
        data = self.normalize_cpf_cnpj(value)
        if len(data) == 11:
            if not check_cpf(data):
                raise ValidationError("CPF is wrong.", field_name="cpf_cnpj")

        elif len(data) == 14:
            pass

        else:
            raise ValidationError("Field cpf_cnpj is wrong", field_name="cpf_cnpj")


class JobSchema(Schema):
    id = Str()
    title = Str(required=True)
    description = Str(required=True)
    cpf_cnpj = Str(required=True)
    date = DateTime(required=True)
    priority = Int(required=True, default=0)
    status = Str(required=True)
    creator_id = Str(required=True)
    creator_email = Str(required=True)


class CreateJobOutput(JobSchema):
    pass


class PaginationJobsOutput(Schema):
    page = Int(required=True)
    per_page = Int(required=True)
    total = Int(required=True)
    items = List(Nested(JobSchema(many=True)), sourceKey='items')
    has_next = Boolean(required=True)
    has_prev = Boolean(required=True)
    next_num = Int(required=True)
    prev_num = Int(required=True)
