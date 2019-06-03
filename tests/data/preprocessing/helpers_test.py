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


