import pandas as pd
from compiler.data.preprocessing import match_goals


def test_pre_process_historic_data_set_returns_a_pre_processed_data_frame():
    df = pd.read_csv("/opt/tests/test-data/test-data.csv")

    reduced = df[-100:]

    pre_processed = match_goals.pre_process_historic_data_set(results=reduced)

    row = pre_processed.iloc[-1, :]

    print(row[['homeShotTargetRatio', 'homeShotSaveRatio', 'awayShotTargetRatio', 'awayShotSaveRatio']])

    assert row['homeShotTargetRatio'] == 0.43
    assert row['homeShotSaveRatio'] == 1
    assert row['awayShotTargetRatio'] == 0.18
    assert row['awayShotSaveRatio'] == 0.33
    assert row['homeAvgScored'] == 2.00
    assert row['homeAvgConceded'] == 0.67
    assert row['awayAvgScored'] == 2.00
    assert row['awayAvgConceded'] == 1.00
