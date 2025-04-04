class Config(object):
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'production_uri'

class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = "sqlite:///to-do-app.db"

class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'testing_uri'
    TESTING = True