import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = 'Alidi-TSD-Service-Key'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:q1W2e3@45.9.27.219:7425/alidi-tsd-service' ##os.environ['DATABASE_URL']


class StagingConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:q1W2e3@45.9.27.219:7425/alidi-tsd-service-test' ##os.environ['DATABASE_URL']


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:q1W2e3@45.9.27.219:7425/alidi-tsd-service-test' ##os.environ['DATABASE_URL']
