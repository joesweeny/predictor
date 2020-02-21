import os

CONNECTIONS = {
    'redis': {
        'host': os.getenv('REDIS_HOST', 'redis.statistico.internal'),
        'port': os.getenv('REDIS_PORT', 6379),
        'database': os.getenv('REDIS_DATABASE', 0)
    },

    'data-server': {
        'host': os.getenv('DATA_SERVER_HOST', 'data-grpc.statistico.internal'),
        'port': os.getenv('DATA_SERVER_PORT', '50051')
    }
}

SUPPORTED_COMPETITIONS = {
    0: {
        'id': 8,
        'name': 'English Premier League',
        'seasons': [
            {
                'id': 10,
                'name': "2015/2016",
            },
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
                'name': "2018/2019",
            },
            {
                'id': 16036,
                'name': "2019/2020",
            }
        ]
    },
}
