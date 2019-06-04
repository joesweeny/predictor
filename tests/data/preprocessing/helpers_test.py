import pytest
import pandas as pd
from datetime import datetime
from predictor.data.preprocessing import helpers


def test_append_and_sort_by_column_combines_data_frames_and_sorts_by_column_provided():
    pd1 = pd.DataFrame([
        {
            'date': pd.to_datetime(datetime.fromisoformat('2019-04-30 18:15:38')),
        },

    ])
    pd2 = pd.DataFrame([
        {
            'date': pd.to_datetime(datetime.fromisoformat('2019-04-23 20:15:38')),
        }
    ])
    pd3 = pd.DataFrame([
        {
            'date': pd.to_datetime(datetime.fromisoformat('2019-04-12 18:15:38')),
        }
    ])

    dfs = [pd1, pd2, pd3]

    combined = helpers.append_and_sort_by_column(dfs=dfs, col='date', asc=True)

    assert [pd.Timestamp('2019-04-12 18:15:38')] == combined.iloc[0, :].tolist()
    assert [pd.Timestamp('2019-04-23 20:15:38')] == combined.iloc[1, :].tolist()
    assert [pd.Timestamp('2019-04-30 18:15:38')] == combined.iloc[2, :].tolist()
    assert (3, 1) == combined.shape


def test_create_over_goals_target_variable_columns_adds_additional_column_to_data_frame():
    row1 = {
        'homeGoals': 1,
        'awayGoals': 2
    }

    row2 = {
        'homeGoals': 0,
        'awayGoals': 2
    }

    row3 = {
        'homeGoals': 4,
        'awayGoals': 2
    }

    df = pd.DataFrame([row1, row2, row3])

    updated = helpers.create_over_goals_target_variable_column(df=df, goals=2.5)

    last_column = updated.iloc[:, -1]

    assert ['awayGoals', 'homeGoals', 'over2.5Goals'] == updated.columns.tolist()
    assert 1 == last_column[0]
    assert 0 == last_column[1]
    assert 1 == last_column[2]


def test_map_formations_converts_string_formations_into_integer_representation():
    row1 = {
        'homeTeam': 'West Ham United',
        'formation': '4-2-2-2'
    }

    row2 = {
        'homeTeam': 'Newcastle United',
        'formation': '4-5-1'
    }

    row3 = {
        'homeTeam': 'Manchester United',
        'formation': '3-4-2-1'
    }

    df = pd.DataFrame([row1, row2, row3])

    mapped = helpers.map_formations(df=df)

    assert 19 == mapped.iloc[0, :]['formation']
    assert 5 == mapped.iloc[1, :]['formation']
    assert 6 == mapped.iloc[2, :]['formation']


def test_drop_non_features_removes_columns_from_data_frame():
    row = {
        'matchID': 23,
        'date': pd.to_datetime(datetime.fromisoformat('2019-04-30 18:15:38')),
        'round': 38,
        'season': '2018/2019',
        'homeTeamID': 45,
        'homeTeam': 'Newcastle United',
        'homeGoals': 0,
        'homeShotsTotal': 5,
        'homeShotsOnGoal': 3,
        'awayTeamID': 1,
        'awayTeam': 'West Ham United',
        'awayGoals': 3,
        'awayShotsTotal': 15,
        'awayShotsOnGoal': 13,
    }

    df = pd.DataFrame([row, row])

    updated = helpers.drop_non_features(df=df)

    columns = [
        'awayShotsOnGoal',
        'awayShotsTotal',
        'homeShotsOnGoal',
        'homeShotsTotal',
    ]

    updated_row = [
        13,
        15,
        3,
        5
    ]

    assert columns == updated.columns.tolist()
    assert updated_row == updated.iloc[0, :].tolist()
    assert updated_row == updated.iloc[1, :].tolist()
    assert (2, 4) == updated.shape


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


def test_set_unknown_features_creates_adds_rolling_averages_for_feature_columns():
    columns = [
        'homeTeam',
        'homeFormation',
        'homeShotsTotal',
        'homeShotsOnGoal',
        'homeShotsOffGoal',
        'homeShotsInsideBox',
        'homeShotsOutsideBox',
        'homeAttacksTotal',
        'homeAttacksDangerous',
        'awayTeam',
        'awayFormation',
        'awayShotsTotal',
        'awayShotsOnGoal',
        'awayShotsOffGoal',
        'awayShotsInsideBox',
        'awayShotsOutsideBox',
        'awayAttacksTotal',
        'awayAttacksDangerous',
    ]

    df = pd.DataFrame(
        [
            add_stats_row('West Ham United', 'Manchester United', 5, 3),
            add_stats_row('Newcastle United', 'Manchester City', 10, 2),
            add_stats_row('Tottenham Hotspur', 'Arsenal', 6, 2),
            add_stats_row('Manchester United', 'Newcastle United', 15, 4),
            add_stats_row('Manchester City', 'West Ham United', 5, 3),
            add_stats_row('Chelsea', 'Watford', 5, 1),
            add_stats_row('Watford', 'Newcastle United', 9, 3),
            add_stats_row('Arsenal', 'Chelsea', 10, 9),
            add_stats_row('West Ham United', 'Tottenham Hotspur', 12, 8),
            add_stats_row('Manchester United', 'Manchester City', 5, 2),
            add_stats_row('Newcastle United', 'Manchester United', 8, 7),
            add_stats_row('West Ham United', 'Manchester United', 5, 3),
            add_stats_row('Newcastle United', 'Manchester City', 10, 2),
            add_stats_row('Tottenham Hotspur', 'Arsenal', 6, 2),
            add_stats_row('Manchester United', 'Newcastle United', 15, 4),
            add_stats_row('Manchester City', 'West Ham United', 5, 3),
            add_stats_row('Chelsea', 'Watford', 5, 1),
            add_stats_row('Watford', 'Newcastle United', 9, 3),
            add_stats_row('Arsenal', 'Chelsea', 10, 9),
            add_stats_row('West Ham United', 'Tottenham Hotspur', 12, 8),
            add_stats_row('Manchester United', 'Manchester City', 5, 2),
            add_stats_row('Newcastle United', 'Manchester United', 8, 7),
            add_stats_row('West Ham United', 'Manchester United', 15, 3),
            add_stats_row('Newcastle United', 'Manchester City', 10, 2),
            add_stats_row('Tottenham Hotspur', 'Arsenal', 6, 2),
            add_stats_row('Manchester United', 'Newcastle United', 15, 4),
            add_stats_row('Manchester City', 'West Ham United', 5, 3),
            add_stats_row('Chelsea', 'Watford', 5, 1),
            add_stats_row('Watford', 'Newcastle United', 9, 3),
            add_stats_row('Arsenal', 'Chelsea', 10, 9),
            add_stats_row('West Ham United', 'Tottenham Hotspur', 12, 8),
            add_stats_row('Manchester United', 'Manchester City', 5, 2),
            add_stats_row('Newcastle United', 'Manchester United', 8, 7),
        ],
        columns=columns
    )

    calculated = helpers.set_unknown_features(df=df, span=5)

    expected_row = [
        'Newcastle United',
        9.260663507109005,
        18.52132701421801,
        9.260663507109005,
        7.696682464454975,
        9.260663507109005,
        3.8483412322274875,
        33.308056872037916,
        3.8483412322274875,
        'Manchester United',
        8.95734597156398,
        13.436018957345969,
        8.95734597156398,
        9.947867298578197,
        4.47867298578199,
        9.947867298578197,
        19.895734597156395,
        4.47867298578199
    ]

    assert expected_row == calculated.iloc[-1, :].tolist()


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


def add_stats_row(home_team: str, away_team: str, high: float, low: float) -> dict:
    row = {
        'homeTeam': home_team,
        'homeFormation': high * 1,
        'homeShotsTotal': high * 2,
        'homeShotsOnGoal': high,
        'homeShotsOffGoal': low * 2,
        'homeShotsInsideBox': high,
        'homeShotsOutsideBox': low,
        'homeAttacksTotal': high * low,
        'homeAttacksDangerous': low,
        'awayTeam': away_team,
        'awayFormation': low * 2,
        'awayShotsTotal': low * 3,
        'awayShotsOnGoal': low * 2,
        'awayShotsOffGoal': high,
        'awayShotsInsideBox': low,
        'awayShotsOutsideBox': high,
        'awayAttacksTotal': high * 2,
        'awayAttacksDangerous': low,
    }

    return row
