"""
Configuration and environment variables to setup the app.
"""
import os
import logging
import logging.config
from datetime import datetime


BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# -------
# Logging
# -------


LOGS_DIR = os.path.expanduser(os.path.join('~', 'logs', 'location_tracker'))

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

LAUNCH_TIME = datetime.now().strftime('%H_%M_%S_%y_%m_%d')

LOG_FILE = os.path.join(LOGS_DIR, '%s.log' % LAUNCH_TIME)

LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'brief': {
            'format': '[%(asctime)s][%(levelname)-8s] %(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        },
        'full': {
            'format': '%(asctime)s|'
                      '%(levelname)-8s|'
                      '%(module)s.%(funcName)s:%(lineno)d|'
                      '%(message)s',
            'datefmt': '%Y-%m-%d %H:%M:%S'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'brief'
        },
        'file': {
            'class': 'logging.FileHandler',
            'formatter': 'full',
            'filename': LOG_FILE
        }
    },
    'loggers': {
        'main': {
            'propagate': False,
            'handlers': ['console', 'file'],
            'level': 'DEBUG'
        },
        'errors': {
            'propagate': False,
            'handlers': ['file'],
            'level': 'WARNING'
        }
    }
}


def get_logger(name='main', level=logging.INFO, dict_conf=LOGGING_CONFIG):
    """A utility to simplify logger initialization."""

    logging.config.dictConfig(dict_conf)
    log = logging.getLogger(name)
    log.setLevel(level=level)
    return log


def env_var(var_name):
    if var_name not in os.environ:
        missing_env_var(var_name)
    return os.environ[var_name]


def missing_env_var(var_name):
    raise RuntimeError(
        f'The environment variable {var_name} is not defined but is '
        f'required to setup the app.')


# ------------------
# App configurations
# ------------------


class Config:
    SECRET_KEY = 'hard to guess string'
    SECURITY_PASSWORD_SALT = 'secret'
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = env_var('APP_DB_URL_DEV')


class TestingConfig(Config):
    TESTING = True
    SECRET_KEY = env_var('APP_SECRET')
    SQLALCHEMY_DATABASE_URI = env_var('APP_DB_URL_TEST')


class ProductionConfig(Config):
    SECRET_KEY = env_var('APP_SECRET')
    SQLALCHEMY_DATABASE_URI = env_var('APP_DB_URL_PROD')


# ------------------
# Configs dictionary
# ------------------


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}

config['default'] = config['development']
