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
                'id': 12,
                'name': "2014/2015",
            },
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
                'name': "2018/2019"
            },
        ]
    },
    # 1: {
    #     'id': 573,
    #     'name': 'Allsvenskan',
    #     'seasons': [
    #         {
    #             'id': 848,
    #             'name': "2017",
    #         },
    #         {
    #             'id': 11759,
    #             'name': "2018",
    #         },
    #         {
    #             'id': 15529,
    #             'name': "2019"
    #         },
    #     ]
    # },
}
