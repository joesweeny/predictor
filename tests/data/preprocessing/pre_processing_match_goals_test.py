import pandas as pd
from compiler.data.preprocessing import match_goals


def test_pre_process_historic_data_set_returns_a_pre_processed_data_frame():
    df = pd.read_csv("/opt/tests/test-data/test-data.csv")

    reduced = df[-100:]

    pre_processed = match_goals.pre_process_historic_data_set(results=reduced)

    row = pre_processed.iloc[-1, :]

    assert row['homeElo'] == 1451.75
    assert row['awayElo'] == 1504.38
    assert row['homeAttackStrength'] == 1533.7
    assert row['homeDefenceStrength'] == 1435.89
    assert row['awayAttackStrength'] == 1541.85
    assert row['awayDefenceStrength'] == 1464.85


def test_pre_process_fixture_data_returns_pre_processed_fixture_data_frame():
    df = pd.read_csv("/opt/tests/test-data/test-data.csv")
    fixture = pd.read_csv("/opt/tests/test-data/test-fixture.csv")

    reduced = df[-100:]
    fixture = fixture.iloc[0, :]

    pre_processed = match_goals.pre_process_fixture_data(fixture=fixture, results=reduced)

    print(pre_processed)

    # assert row['homeXGFor'] == 1.48
    # assert row['homeXGAgainst'] == 1.18
    # assert row['awayXGFor'] == 1.49
    # assert row['awayXGAgainst'] == 0.72
    # assert row['homeAvgScored'] == 2.67
    # assert row['homeAvgConceded'] == 1.67
    # assert row['awayAvgScored'] == 1.33
    # assert row['awayAvgConceded'] == 0.67
    # assert row['homeShotTargetRatio'] == 0.43
    # assert row['homeShotSaveRatio'] == 0.61
    # assert row['awayShotTargetRatio'] == 0.43
    # assert row['awayShotSaveRatio'] == 0.85
