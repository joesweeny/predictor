import pandas as pd
from compiler.models.total_goals import preprocessing


def test_prepare_dataframe_returns_prepared_dataframe():
    df = pd.DataFrame.from_dict(__get_data())

    stats = {
        '2019/2020': {
            2: [
                {
                    'team': 'Chelsea',
                    'position': 1,
                    'goals': 25,
                    'diff': 0,
                },
                {
                    'team': 'Arsenal',
                    'position': 3,
                    'goals': 22,
                    'diff': 0,
                }
            ],
            3: [
                {
                    'team': 'West Ham United',
                    'position': 1,
                    'goals': 28,
                    'diff': 0,
                },
                {
                    'team': 'Chelsea',
                    'position': 2,
                    'goals': 26,
                    'diff': 1,
                },
            ]
        }
    }

    prepped = preprocessing.prepare_dataframe(df, stats)

    assert len(prepped) == 2

    assert prepped.iloc[0]['homeTeam'] == 'Arsenal'
    assert prepped.iloc[0]['awayTeam'] == 'Chelsea'
    assert prepped.iloc[0]['homePosition'] == 3
    assert prepped.iloc[0]['homePosDiff'] == 0
    assert prepped.iloc[0]['awayPosition'] == 1
    assert prepped.iloc[0]['awayPosDiff'] == 0

    assert prepped.iloc[1]['homeTeam'] == 'Chelsea'
    assert prepped.iloc[1]['awayTeam'] == 'West Ham United'
    assert prepped.iloc[1]['homePosition'] == 2
    assert prepped.iloc[1]['homePosDiff'] == 1
    assert prepped.iloc[1]['awayPosition'] == 1
    assert prepped.iloc[1]['awayPosDiff'] == 0


def test_prepare_dataframe_can_handle_missing_data_and_filters_rows_out():
    df = pd.DataFrame.from_dict(__get_data())

    stats = {
        '2019/2020': {
            2: [
                {
                    'team': 'Chelsea',
                    'position': 1,
                    'goals': 25,
                    'diff': 0,
                },
            ],
            3: [
                {
                    'team': 'West Ham United',
                    'position': 1,
                    'goals': 28,
                    'diff': 0,
                },
                {
                    'team': 'Chelsea',
                    'position': 2,
                    'goals': 26,
                    'diff': 1,
                },
            ]
        }
    }

    prepped = preprocessing.prepare_dataframe(df, stats)

    assert len(prepped) == 1
    assert prepped.iloc[0]['homeTeam'] == 'Chelsea'
    assert prepped.iloc[0]['awayTeam'] == 'West Ham United'
    assert prepped.iloc[0]['homePosition'] == 2
    assert prepped.iloc[0]['homePosDiff'] == 1
    assert prepped.iloc[0]['awayPosition'] == 1
    assert prepped.iloc[0]['awayPosDiff'] == 0


def __get_data():
    data = {
        'round': [
            1,
            2,
            3,
        ],
        'season': [
            '2019/2020',
            '2019/2020',
            '2019/2020',
        ],
        'homeTeam': [
            'West Ham United',
            'Arsenal',
            'Chelsea'
        ],
        'awayTeam': [
            'Arsenal',
            'Chelsea',
            'West Ham United'
        ],
    }

    return data
