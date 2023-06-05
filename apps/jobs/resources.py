# Python

# Flask
from flask import request, current_app

# Third
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
from marshmallow import fields
# Apps
from apps.extensions.messages import MSG_RESOURCE_CREATED, MSG_RESOURCE_FETCHED_PAGINATED
from apps.extensions.responses import resp_ok, resp_data_invalid, resp_does_not_exist, resp_exception

# Local
from .commands import CreateJobCommand, GetJobsPaginatedCommand, GetJobCommand
from .schemas import CreateJobInput, CreateJobOutput, PaginationJobsOutput, JobSchema



class JobsResource(MethodResource, Resource):

    @doc(description='Listar os jobs criados pelo usuario paginado', tags=['Jobs'])
    @marshal_with(PaginationJobsOutput)
    @use_kwargs({"page": fields.Integer(), "per_page": fields.Integer() }, location="query",  apply=False)
    @jwt_required()
    def get(self, *args, **kwargs):
        params = request.args
        claims = get_jwt()

        user_id = claims["user_id"]
        kwargs.update({ 'creator_id': user_id, 'page': int(params['page']), 'per_page': int(params['per_page']) })

        try:
            output = GetJobsPaginatedCommand.run(*args, **kwargs)
            # Retorno 200 o meu endpoint
            return resp_ok(
                'Jobs', MSG_RESOURCE_FETCHED_PAGINATED.format('Jobs'),  data=output,
            )
        except Exception as exc:
            return resp_exception(
                resource='jobs',
                description='An error occurred',
                msg=exc.__str__()
            )

    @doc(description='Criar uma tarefa para buscar dados de um cnpj', tags=['Jobs'])
    @use_kwargs(CreateJobInput, location=('json'), apply=False)
    @marshal_with(CreateJobOutput)
    @jwt_required()
    def post(self, *args, **kwargs):
        '''
        Route to do login in API
        '''
        # Inicializo todas as variaveis utilizadas

        payload = request.get_json() or None

        claims = get_jwt()

        user_email = get_jwt_identity()
        user_id = claims["user_id"]
        use_queue = current_app.config['USE_QUEUE']
        kwargs.update({'user_id': user_id, 'user_email': user_email, 'use_queue': use_queue})

        try:
            output = CreateJobCommand.run(payload, *args, **kwargs)
            # Retorno 200 o meu endpoint
            return resp_ok(
                'Jobs', MSG_RESOURCE_CREATED.format('Usuário'),  data=output,
            )
        except Exception as exc:
            return resp_exception(
                resource='jobs',
                description='An error occurred',
                msg=exc.__str__()
            )



class JobResource(MethodResource, Resource):

    @doc(description='Buscar os detalhes de um job', tags=['Jobs'])
    @marshal_with(JobSchema)
    @jwt_required()
    def get(self, job_id, *args, **kwargs):
        claims = get_jwt()

        user_id = claims["user_id"]
        kwargs.update({ 'creator_id': user_id, 'job_id': job_id })

        try:
            output = GetJobCommand.run(*args, **kwargs)
            # Retorno 200 o meu endpoint
            return resp_ok(
                'Jobs', MSG_RESOURCE_FETCHED_PAGINATED.format('Jobs'),  data=output,
            )
        except Exception as exc:
            return resp_exception(
                resource='jobs',
                description='An error occurred',
                msg=exc.__str__()
            )


    @doc(description='Atualiza um job', tags=['Jobs'])
    @marshal_with(JobSchema)
    @jwt_required()
    def update(self, job_id, *args, **kwargs):
        pass

    @doc(description='Deletar um job', tags=['Jobs'])
    @jwt_required()
    def delete(self, job_id, *args, **kwargs):
        pass
