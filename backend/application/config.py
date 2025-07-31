class config():
    DEBUG = False
    SQLALCHEMY_TRACK_MODIFICATIONS=True

class LocalDevelopmentConfig(config):
    # configuration
    SQLALCHEMY_DATABASE_URI = "sqlite:///qmv2-3.sqlite3"
    DEBUG = True

    # config for security
    JWT_SECRET_KEY = "this-is-a-secret-key"
    SECRET_KEY = "secret_key"
    WTF_CSRF_ENABLED = False