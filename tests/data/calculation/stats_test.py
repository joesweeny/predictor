import pandas as pd
import pytest
from compiler.data.calculation.stats import calculate_feature_average, calculate_home_advantage


def test_calculate_feature_average_returns_a_calculated_ratio_float_for_feature():
    df = pd.read_csv("/opt/tests/test-data/test-data.csv")
    row = pd.read_csv("/opt/tests/test-data/test-fixture.csv")

    home_xg_for = calculate_feature_average(
        df=df,
        row=row.iloc[0, :],
        home_away='homeTeam',
        feature='homeXGFor',
        rating='awayDefenceStrength',
        factor=50,
        row_count=3
    )

    away_xg_for = calculate_feature_average(
        df=df,
        row=row.iloc[0, :],
        home_away='awayTeam',
        feature='awayXGFor',
        rating='homeDefenceStrength',
        factor=50,
        row_count=3
    )

    home_xg_against = calculate_feature_average(
        df=df,
        row=row.iloc[0, :],
        home_away='homeTeam',
        feature='homeXGAgainst',
        rating='awayAttackStrength',
        factor=50,
        row_count=3
    )

    away_xg_against = calculate_feature_average(
        df=df,
        row=row.iloc[0, :],
        home_away='awayTeam',
        feature='awayXGAgainst',
        rating='homeAttackStrength',
        factor=50,
        row_count=3
    )

    assert home_xg_for == 1.98
    assert away_xg_for == 1.71
    assert home_xg_against == 0.89
    assert away_xg_against == 0.94


def test_calculate_home_advantage_returns_a_float():
    df = pd.read_csv("/opt/tests/test-data/test-data.csv")
    row = pd.read_csv("/opt/tests/test-data/test-fixture.csv")

    assert calculate_home_advantage(row=row.iloc[0, :], df=df, index=1179) == 1.79
