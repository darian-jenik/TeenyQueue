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
        },
    'root': {
        'level': LOG_LEVEL,
        'handlers': ['console']
        }
}

# end
