# Third
from flask_apispec.extension import FlaskApiSpec

# Importamos as classes API e Resource
from flask_restful import Api, Resource
from flask_apispec import marshal_with
from flask_apispec.views import MethodResource
from flask_apispec import marshal_with, doc, use_kwargs
from apps.jobs.resources import CreateJobResource

# Criamos uma classe que extende de Resource
class Index(MethodResource, Resource):

    # Definimos a operação get do protocolo http
    @doc(description='Registrar um usuário/customers', tags=['Customer'])
    # @use_kwargs(CreateUserInput, location=('json'), apply=False)
    # @marshal_with(CreateUserOutput)
    def get(self):

        # retornamos um simples dicionário que será automáticamente
        # retornado em json pelo flask
        return {'hello': 'world by apps'}


# Instânciamos a API do FlaskRestful
api = Api()


def configure_api(app):

    api.add_resource(Index, '/')
    api.add_resource(CreateJobResource, '/jobs')

    # rotas para jobs

    # inicializamos a api com as configurações do flask vinda por parâmetro
    api.init_app(app)

    docs = FlaskApiSpec(app)
    docs.register(Index)
    docs.register(CreateJobResource)
