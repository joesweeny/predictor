import pandas as pd
from compiler.preprocessing.feature_creation.goals import process_historic_data_set, process_fixture_data


def test_pre_process_historic_data_set_returns_a_pre_processed_data_frame():
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


def test_pre_process_fixture_data_returns_pre_processed_fixture_data_frame():
    df = pd.read_csv("/opt/tests/test-data/test-data.csv")
    fixture = pd.read_csv("/opt/tests/test-data/test-fixture.csv")

    reduced = df[-100:]
    fixture = fixture.iloc[0, :]

    row = process_fixture_data(fixture=fixture, results=reduced)

    assert row['fixtureID'] == 10332808
    assert row['date'] == '2018-09-15 11:30:00'
    assert row['round'] == 5
    assert row['season'] == '2018/2019'
    assert row['homeTeam'] == 'Tottenham Hotspur'
    assert row['homeGoalsScored'] == 9
    assert row['homeGoalsConceded'] == 4
    assert row['homeShotsOnGoal'] == 23
    assert row['homeShotsTotal'] == 60
    assert row['homeXGF'] == 8.24
    assert row['homeXGA'] == 4.26
    assert row['homeAttackStrength'] == 1816.55
    assert row['homeDefenceStrength'] == 1526.98

    assert row['awayTeam'] == 'Liverpool'
    assert row['awayGoalsScored'] == 9
    assert row['awayGoalsConceded'] == 1
    assert row['awayShotsOnGoal'] == 26
    assert row['awayShotsTotal'] == 66
    assert row['awayXGF'] == 10.20
    assert row['awayXGA'] == 2.29
    assert row['awayAttackStrength'] == 1752.04
    assert row['awayDefenceStrength'] == 1395.45
