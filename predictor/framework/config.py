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
                'id': 1586,
                'name': "2005/2006",
            },
            {
                'id': 8,
                'name': "2006/2007",
            },
            {
                'id': 14,
                'name': "2007/2008",
            },
            {
                'id': 6,
                'name': "2008/2009",
            },
            {
                'id': 11,
                'name': "2009/2010",
            },
            {
                'id': 9,
                'name': "2011/2012",
            },
            {
                'id': 7,
                'name': "2012/2013",
            },
            {
                'id': 3,
                'name': "2013/2014",
            },
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
}
