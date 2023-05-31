import os

from flask import Flask


# from datetime import datetime
# from datetime import timedelta
# from datetime import timezone
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin

# Realize a importação da função que configura a api
from apps.extensions.api import configure_api
from apps.extensions.config import config
from apps.extensions.db import db
from apps.extensions.jwt import configure_jwt


def create_app(testing=False):
    app = Flask('agendador-de-consultas-de-cnpj')

    config_name = os.getenv("FLASK_CONFIG", 'default')

    if testing:
        app.config.from_object(config['testing'])

    else:
        app.config.from_object(config[config_name])

    app.config.update({
        'APISPEC_SPEC': APISpec(
            title='Flask Api Users',
            version='v1',
            plugins=[MarshmallowPlugin()],
            openapi_version='2.0.0'
        ),
        'APISPEC_SWAGGER_URL': '/swagger/',  # URI to access API Doc JSON
        'APISPEC_SWAGGER_UI_URL': '/swagger-ui/'  # URI to access UI of API Doc
    })

    # Configure MongoEngine
    db.init_app(app)

    # Configure JWT
    configure_jwt(app)

    # executa a chamada da função de configuração
    configure_api(app)

    return app

# app = create_app()
