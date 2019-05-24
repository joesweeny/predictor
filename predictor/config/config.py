import os

CONNECTIONS = {
    'redis': {
        'host': os.getenv('REDIS_HOST'),
        'port': os.getenv('REDIS_PORT'),
        'database': os.getenv('REDIS_DATABASE')
    }
}

