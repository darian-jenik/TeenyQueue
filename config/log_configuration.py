# config/log_configuration.py

import os

LOG_FORMAT = '[%(asctime)s] %(levelname)s [%(lineno)s:[%(module)s:%(funcName)s]] %(message)s'
LOG_LEVEL = os.environ.get('TQ_LOG_LEVEL', 'INFO').upper()

# Note: The stupid thing doesn't like underscores in name keys!!
loggingConfig = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
            'default': {
                'class': 'logging.Formatter',
                'format': LOG_FORMAT,
            }
        },
    'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'stream': 'ext://sys.stdout',
                'level': LOG_LEVEL,
            }
        },
    'loggers': {
            'tqlogger': {
                'class': 'TQCustomLogger',
                'level': 'INFO',
                'handlers': [],
                'propagate': True
            },
            'uvicorn': {
                'class': 'TQCustomLogger',
                'level': 'INFO',
                'handlers': [],
                'propagate': False
            },
            'uvicorn.error': {
                'class': 'TQCustomLogger',
                'level': 'INFO',
                'handlers': [],
                'propagate': False
            },
            'uvicorn.access': {
                'class': 'TQCustomLogger',
                'level': 'INFO',
                'handlers': [],
                'propagate': False
            },
            'fastapi': {
                'class': 'TQCustomLogger',
                'level': 'INFO',
                'handlers': [],
                'propagate': False
            },
        },
    'root': {
        'class': 'TQCustomLogger',
        'level': LOG_LEVEL,
        'handlers': ['console']
        }
}

# end
