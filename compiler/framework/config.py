import os


def config_factory():
    return {
        'connections': {
            'redis': {
                'host': os.getenv('REDIS_HOST', 'redis'),
                'port': os.getenv('REDIS_PORT', 6379),
                'database': os.getenv('REDIS_DATABASE', 15)
            },

            'data_server': {
                'host': os.getenv('DATA_SERVER_HOST', 'statistico-data-grpc'),
                'port': os.getenv('DATA_SERVER_PORT', '50051')
            }
        },
        'supported_competitions': [
            {
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
                        'name': "2018/2019",
                    },
                    {
                        'id': 16036,
                        'name': "2019/2020",
                    },
                    {
                        'id': 17420,
                        'name': "2020/2021",
                    }
                ]
            },
            {
                'id': 82,
                'name': 'Bundesliga',
                'seasons': [
                    {
                        'id': 217,
                        'name': "2014/2015",
                    },
                    {
                        'id': 218,
                        'name': "2015/2016",
                    },
                    {
                        'id': 219,
                        'name': "2016/2017",
                    },
                    {
                        'id': 8026,
                        'name': "2017/2018",
                    },
                    {
                        'id': 13005,
                        'name': "2018/2019",
                    },
                    {
                        'id': 16264,
                        'name': "2019/2020",
                    },
                    {
                        'id': 17361,
                        'name': "2020/2021",
                    }
                ]
            },
            {
                'id': 564,
                'name': 'La Liga',
                'seasons': [
                    {
                        'id': 2061,
                        'name': "2014/2015",
                    },
                    {
                        'id': 2063,
                        'name': "2015/2016",
                    },
                    {
                        'id': 853,
                        'name': "2016/2017",
                    },
                    {
                        'id': 8442,
                        'name': "2017/2018",
                    },
                    {
                        'id': 13133,
                        'name': "2018/2019",
                    },
                    {
                        'id': 16326,
                        'name': "2019/2020",
                    },
                    {
                        'id': 17480,
                        'name': "2020/2021",
                    }
                ]
            },
            {
                'id': 384,
                'name': 'Serie A',
                'seasons': [
                    {
                        'id': 1583,
                        'name': "2014/2015",
                    },
                    {
                        'id': 1584,
                        'name': "2015/2016",
                    },
                    {
                        'id': 802,
                        'name': "2016/2017",
                    },
                    {
                        'id': 8557,
                        'name': "2017/2018",
                    },
                    {
                        'id': 13158,
                        'name': "2018/2019",
                    },
                    {
                        'id': 16415,
                        'name': "2019/2020",
                    },
                    {
                        'id': 17488,
                        'name': "2020/2021",
                    }
                ]
            },
        ]
    }
