import logging
from logging.config import dictConfig
from pythonjsonlogger import jsonlogger

class JsonFormatter(logging.Formatter):
    def format(self, record):

        formatter = jsonlogger.JsonFormatter(
            '%(asctime)s %(name)s %(levelname)s %(message)s'
        )
        return formatter.format(record)

def setup_logging():
    config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            'default': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            },
            'json': {
                '()': JsonFormatter,
            },
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'formatter': 'default',
                'level': 'INFO',
            },
             'console_json': {
                'class': 'logging.StreamHandler',
                'formatter': 'json',
                'level': 'INFO',
            },
        },
        'loggers': {
            '': {  # root logger
                'handlers': ['console_json'],
                'level': 'INFO',
            },
            'uvicorn.error': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
            'uvicorn.access': {
                'handlers': ['console'],
                'level': 'INFO',
                'propagate': False,
            },
        },
    }
    dictConfig(config)
