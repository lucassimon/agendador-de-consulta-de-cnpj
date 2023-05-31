# Python
from os import getenv


class Config:
    SECRET_KEY = getenv('SECRET_KEY')
    PORT = int(getenv('PORT', 8080))
    DEBUG = getenv('DEBUG') or False
    SQLALCHEMY_DATABASE_URI = getenv['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    FLASK_ENV = 'development'
    # always
    DEBUG = True


class TestingConfig(Config):
    FLASK_ENV = 'testing'
    TESTING = True


class ProductionConfig(Config):
    FLASK_ENV = 'production'
    TESTING = False
    DEBUG = False


config = {
    'production': ProductionConfig,
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
