import pandas as pd
from compiler.preprocessing.feature_creation.goals import process_fixture_data


def test_process_fixture_data_returns_pre_processed_fixture_series_object():
    df = pd.read_csv("/opt/tests/test-data/test-data.csv")
    fixture = pd.read_csv("/opt/tests/test-data/test-fixture.csv")

    reduced = df[-100:]
    fixture = fixture.iloc[0, :]

    row = process_fixture_data(fixture=fixture, results=reduced)

    row = row.reshape(-1)

    assert row[0] == 1.0
    assert row[1] == 0.8214285714285714
    assert row[2] == 0.8870967741935484
    assert row[3] == 0.5454545454545455
    assert row[4] == 0.9999999999999999
    assert row[5] == 1.0
    assert row[6] == 0.4444444444444444
    assert row[7] == 0.9727047146401984
    assert row[8] == 0.5202156334231804
    assert row[9] == 1.0
    assert row[10] == 1.0
    assert row[11] == 0.4583333333333333
    assert row[12] == 0.4814814814814815
    assert row[13] == 1.0
    assert row[14] == 0.1111111111111111
    assert row[15] == 1.0
    assert row[16] == 0.24966974900924704
    assert row[17] == 0.8118495906757328
    assert row[18] == 0.08649439297903427
    assert row[19] == 0.6628564966529833
    assert row[20] == 0.7168761069410472
