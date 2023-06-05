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
from apps.extensions.messages import MSG_RESOURCE_FETCHED_PAGINATED
from apps.extensions.responses import resp_ok, resp_exception

# Local
from .commands import GetAllResultsCommand
from .schemas import ResultSchema



class ResultsResource(MethodResource, Resource):

    @doc(description='Listar os resultados de uma tarefa', tags=['Results'])
    @marshal_with(ResultSchema)
    @use_kwargs({"job_id": fields.Integer(), }, location="query",  apply=False)
    @jwt_required()
    def get(self, *args, **kwargs):
        params = request.args
        claims = get_jwt()

        user_id = claims["user_id"]
        kwargs.update({ 'creator_id': user_id, 'job_id': int(params['job_id']), })

        try:
            output = GetAllResultsCommand.run(*args, **kwargs)
            # Retorno 200 o meu endpoint
            return resp_ok(
                'Results', MSG_RESOURCE_FETCHED_PAGINATED.format('Results'),  data=output,
            )

        except Exception as exc:
            return resp_exception(
                resource='results',
                description='An error occurred',
                msg=exc.__str__()
            )
