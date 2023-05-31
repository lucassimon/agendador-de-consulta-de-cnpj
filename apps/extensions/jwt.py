# Flask

# Third
from flask_jwt_extended import JWTManager
# Apps


def configure_jwt(app):

    # Add jwt handler
    jwt = JWTManager(app)