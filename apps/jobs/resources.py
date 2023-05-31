# Python

# Flask
from flask import request

# Third
from flask_restful import Resource
from flask_jwt_extended import create_access_token
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_apispec import marshal_with, doc, use_kwargs
from flask_apispec.views import MethodResource
# Apps
from apps.extensions.messages import MSG_TOKEN_CREATED
from apps.extensions.responses import resp_ok, resp_data_invalid, resp_does_not_exist, resp_exception
from apps.users.exceptions import UserMongoDoesNotExistException
from apps.users.schemas import UserSchema

# Local



class JobResource(MethodResource, Resource):

    @doc(description='Criar uma tarefa para buscar dados de um cnpj', tags=['Jobs'])
    # @use_kwargs(LoginSchema, location=('json'), apply=False)
    @marshal_with(UserSchema)
    def post(self, *args, **kwargs):
        '''
        Route to do login in API
        '''
        # Inicializo todas as variaveis utilizadas
        payload = request.get_json() or None
