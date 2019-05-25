import os

CONNECTIONS = {
    'redis': {
        'host': os.getenv('REDIS_HOST'),
        'port': os.getenv('REDIS_PORT'),
        'database': os.getenv('REDIS_DATABASE')
    }
}

SUPPORTED_COMPETITIONS = {
    0: {
        'id': 1,
        'name': 'English Premier League',
        'seasons': {
            13: "2016/2017",
            6397: "2017/2018",
            12962: "2018/2019",
        }
    }
}
