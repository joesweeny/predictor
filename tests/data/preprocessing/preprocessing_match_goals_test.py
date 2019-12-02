import pandas as pd
from compiler.data.preprocessing import match_goals


def test_pre_process_historic_data_set_returns_a_pre_processed_data_frame():
    df = pd.read_csv("/opt/tests/test-data/test-data.csv")

    reduced = df[-100:]

    pre_processed = match_goals.pre_process_historic_data_set(results=reduced)

    row = pre_processed.iloc[-1, :]

    assert row['homeAdvantage'] == 1.6
    assert row['homeXGFor'] == 2.75
    assert row['homeXGAgainst'] == 1.15
    assert row['awayXGFor'] == 0.92
    assert row['awayXGAgainst'] == 2.38
    assert row['homeAvgScored'] == 2.5
    assert row['homeAvgConceded'] == 1.33
    assert row['awayAvgScored'] == 1.0
    assert row['awayAvgConceded'] == 2.33


def test_pre_process_fixture_data_returns_pre_processed_fixture_data_frame():
    df = pd.read_csv("/opt/tests/test-data/test-data.csv")
    fixture = pd.read_csv("/opt/tests/test-data/test-fixture.csv")

    reduced = df[-100:]

    pre_processed = match_goals.pre_process_fixture_data(fixture=fixture, results=reduced)

    row = pre_processed.iloc[-1, :]

    assert row['homeAdvantage'] == 1.0
    assert row['homeXGFor'] == 1.78
    assert row['homeXGAgainst'] == 0.93
    assert row['awayXGFor'] == 1.69
    assert row['awayXGAgainst'] == 0.85
    assert row['homeAvgScored'] == 1.67
    assert row['homeAvgConceded'] == 1.33
    assert row['awayAvgScored'] == 1.67
    assert row['awayAvgConceded'] == 1.0
