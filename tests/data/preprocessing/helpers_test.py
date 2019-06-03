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


# revert_elos_to_mean


# elo_calculator


# apply_historic_elos


# apply_current_elos


# map_formations
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

# drop_non_features


# set_unknown_features
