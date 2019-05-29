import os

CONNECTIONS = {
    'redis': {
        'host': os.getenv('REDIS_HOST'),
        'port': os.getenv('REDIS_PORT'),
        'database': os.getenv('REDIS_DATABASE')
    },

    'data-server': {
        'host': os.getenv('DATA_SERVER_HOST'),
        'port': os.getenv('DATA_SERVER_PORT')
    }
}

SUPPORTED_COMPETITIONS = {
    0: {
        'id': 8,
        'name': 'English Premier League',
        'seasons': [
            {
                'id': 13,
                'name': "2016/2017",
            },
            {
                'id': 6397,
                'name': "2017/2018",
            },
            {
                'id': 12962,
                'name': "2018/2019"
            },
        ]
    }
}
