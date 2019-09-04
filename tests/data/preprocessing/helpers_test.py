import pytest
import pandas as pd
from datetime import datetime
from compiler.data.preprocessing import helpers


def test_elo_calculator_returns_three_lists_containing_elo_calculations(elos_df):
    elos, elos_probs, elos_current = helpers.elo_calculator(
        df=elos_df,
        k_factor=25,
        historic_elos={team: 1500 for team in elos_df['homeTeam'].unique()},
        soft_reset_factor=0.96,
        match_id_column='matchID'
    )

    expected_elos = {
        1: [
            1500.0,
            1500.0,
        ],
        2: [
            1500.0,
            1500.0
        ],
        3: [
            1500,
            1518.75
        ],
        4: [
            1500.0,
            1481.25,
        ],
        5: [
            1469.42,
            1479.3
        ]
    }

    expected_elos_probs = {
        1: [
            0.5,
            0.5
        ],
        2: [
            0.5,
            0.5
        ],
        3: [
            0.47,
            0.53
        ],
        4: [
            0.53,
            0.47
        ],
        5: [
            0.49,
            0.51
        ]
    }

    expected_elos_current = {
        'West Ham United': 1539.45,
        'Newcastle United': 1466.44,
        'Brighton': 1511.83,
        'Manchester United': 1482.28
    }

    assert elos == expected_elos
    assert elos_probs == expected_elos_probs
    assert elos_current == expected_elos_current


def test_elo_calculator_can_handle_multiple_seasons(elos_df):
    row1 = {
        'matchID': 6,
        'season': '2018/2019',
        'homeTeam': 'West Ham United',
        'awayTeam': 'Manchester United',
        'homeGoals': 2,
        'awayGoals': 1
    }

    row2 = {
        'matchID': 7,
        'season': '2018/2019',
        'homeTeam': 'Newcastle United',
        'awayTeam': 'Brighton',
        'homeGoals': 1,
        'awayGoals': 3
    }

    df = pd.DataFrame([row1, row2])

    df = elos_df.append(df)

    elos, elos_probs, elos_current = helpers.elo_calculator(
        df=df,
        k_factor=25,
        historic_elos={team: 1500 for team in df['homeTeam'].unique()},
        soft_reset_factor=0.96,
        match_id_column='matchID'
    )

    expected_elos = {
        1: [
            1500.0,
            1500.0,
        ],
        2: [
            1500.0,
            1500.0
        ],
        3: [
            1500,
            1518.75
        ],
        4: [
            1500.0,
            1481.25,
        ],
        5: [
            1469.42,
            1479.3
        ],
        6: [
            1537.87,
            1482.99
        ],
        7: [
            1467.78,
            1511.36
        ]
    }

    expected_elos_probs = {
        1: [
            0.5,
            0.5
        ],
        2: [
            0.5,
            0.5
        ],
        3: [
            0.47,
            0.53
        ],
        4: [
            0.53,
            0.47
        ],
        5: [
            0.49,
            0.51
        ],
        6: [
            0.58,
            0.42
        ],
        7: [
            0.44,
            0.56
        ]
    }

    expected_elos_current = {
        'West Ham United': 1548.41,
        'Newcastle United': 1451.37,
        'Brighton': 1527.77,
        'Manchester United': 1472.45
    }

    assert elos == expected_elos
    assert elos_probs == expected_elos_probs
    assert elos_current == expected_elos_current


def test_apply_historic_elos_adds_new_elo_columns_to_data_frame(elos_df):
    elos, elos_probs, elos_current = helpers.elo_calculator(
        df=elos_df,
        k_factor=25,
        historic_elos={team: 1500 for team in elos_df['homeTeam'].unique()},
        soft_reset_factor=0.96,
        match_id_column='matchID'
    )

    elo_applied = helpers.apply_historic_elos(features=elos_df, elos=elos, elo_probs=elos_probs)

    columns = [
        'matchID',
        'homeElo',
        'awayElo',
        'homeEloProb',
        'awayEloProb'
    ]

    assert [1, 1500.0, 1500.0, 0.5, 0.5] == elo_applied.iloc[0, :][columns].tolist()
    assert [2, 1500.0, 1500.0, 0.5, 0.5] == elo_applied.iloc[1, :][columns].tolist()
    assert [3, 1500.0, 1518.75, 0.47, 0.53] == elo_applied.iloc[2, :][columns].tolist()
    assert [4, 1500.0, 1481.25, 0.53, 0.47] == elo_applied.iloc[3, :][columns].tolist()
    assert [5, 1469.42, 1479.3, 0.49, 0.51] == elo_applied.iloc[4, :][columns].tolist()


def test_apply_current_elos_adds_new_elo_columns_to_data_frame(elos_df):
    elos, elos_probs, elos_current = helpers.elo_calculator(
        df=elos_df,
        k_factor=25,
        historic_elos={team: 1500 for team in elos_df['homeTeam'].unique()},
        soft_reset_factor=0.96,
        match_id_column='matchID'
    )

    elo_applied = helpers.apply_current_elos(features=elos_df, elos_current=elos_current)

    columns = [
        'homeElo',
        'awayElo',
        'homeEloProb',
        'awayEloProb'
    ]

    assert [1539.45, 1482.28, 0.58, 0.42] == elo_applied.iloc[0, :][columns].tolist()


@pytest.fixture
def elos_df():
    row1 = {
        'matchID': 1,
        'season': '2017/2018',
        'homeTeam': 'West Ham United',
        'awayTeam': 'Manchester United',
        'homeGoals': 3,
        'awayGoals': 1
    }

    row2 = {
        'matchID': 2,
        'season': '2017/2018',
        'homeTeam': 'Newcastle United',
        'awayTeam': 'Brighton',
        'homeGoals': 1,
        'awayGoals': 1
    }

    row3 = {
        'matchID': 3,
        'season': '2017/2018',
        'homeTeam': 'Newcastle United',
        'awayTeam': 'West Ham United',
        'homeGoals': 0,
        'awayGoals': 3
    }

    row4 = {
        'matchID': 4,
        'season': '2017/2018',
        'homeTeam': 'Brighton',
        'awayTeam': 'Manchester United',
        'homeGoals': 2,
        'awayGoals': 1
    }

    row5 = {
        'matchID': 5,
        'season': '2017/2018',
        'homeTeam': 'Manchester United',
        'awayTeam': 'Newcastle United',
        'homeGoals': 2,
        'awayGoals': 1
    }

    df = pd.DataFrame([row1, row2, row3, row4, row5])

    return df
