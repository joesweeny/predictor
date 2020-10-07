import pandas as pd
from compiler.preprocessing.feature_creation.goals import process_historic_data_set, process_fixture_data


def test_process_historic_data_set_returns_a_pre_processed_data_frame():
    df = pd.read_csv("/opt/tests/test-data/test-data.csv")

    reduced = df[-100:]

    pre_processed = process_historic_data_set(results=reduced)

    row = pre_processed.iloc[-1, :]

    assert row['homeElo'] == 1451.75
    assert row['awayElo'] == 1504.38
    assert row['homeAttackStrength'] == 1533.7
    assert row['homeDefenceStrength'] == 1435.89
    assert row['awayAttackStrength'] == 1541.85
    assert row['awayDefenceStrength'] == 1464.85


def test_process_fixture_data_returns_pre_processed_fixture_series_object():
    df = pd.read_csv("/opt/tests/test-data/test-data.csv")
    fixture = pd.read_csv("/opt/tests/test-data/test-fixture.csv")

    reduced = df[-100:]
    fixture = fixture.iloc[0, :]

    row = process_fixture_data(fixture=fixture, results=reduced)

    assert row[0] == 0.002203189116245766
    assert row[1] == 0.004406378232491532
    assert row[2] == 0.0016523918371843245
    assert row[3] == 0.003987772300404837
    assert row[4] == 0.001795599129740299
    assert row[5] == 0.004406378232491532
    assert row[6] == 0.0
    assert row[7] == 0.0050673349673652605
    assert row[8] == 0.0007105284899892597
    assert row[9] == 1.0
    assert row[10] == 0.8405056319021784
    assert row[11] == 0.9644680675277465
    assert row[12] == 0.768059265787227

