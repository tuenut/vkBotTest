import os
from logging import DEBUG

from utils.paths import init_base_dir_path

NAME = "CoolVkBot"

BASE_DIR = init_base_dir_path()
LOG_DIR = os.path.join(BASE_DIR, '.logs')

LOG_LEVEL = DEBUG
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'basic': {
            '()': 'logging.Formatter',
            'format': '%(asctime)s %(levelname)-8s: %(message)s'
        },
        'verbose': {
            '()': 'logging.Formatter',
            'format': '%(asctime)s %(levelname)-8s [%(name)s:%(lineno)4d]: %(message)s'
        },
    },
    'loggers': {
        '': {
            'level': LOG_LEVEL,
            'handlers': ['basic_stream', 'basic_file'],
            'propagate': True,
        }
    },
    'handlers': {
        'basic_stream': {
            'level': LOG_LEVEL,
            'class': 'logging.StreamHandler',
            'formatter': 'basic',
            "stream": "ext://sys.stdout"
        },
        'basic_file': {
            'level': LOG_LEVEL,
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'maxBytes': 256 * 1024 * 1024,
            'backupCount': 10,
            'filename': os.path.join(LOG_DIR, '{}.log'.format(NAME))
        },
    }
}
