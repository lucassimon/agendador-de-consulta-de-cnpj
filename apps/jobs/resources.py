# Python

# Flask
from flask import request, current_app

# Third
from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
# Apps
from apps.extensions.messages import MSG_RESOURCE_CREATED
from apps.extensions.responses import resp_ok, resp_data_invalid, resp_does_not_exist, resp_exception

# Local
from .commands import CreateJobCommand
from .schemas import CreateJobInput, CreateJobOutput


class CreateJobResource(MethodResource, Resource):

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
                'Users', MSG_RESOURCE_CREATED.format('Usuário'),  data=output,
            )
        except Exception as exc:
            return resp_exception(
                resource='users',
                description='An error occurred',
                msg=exc.__str__()
            )
