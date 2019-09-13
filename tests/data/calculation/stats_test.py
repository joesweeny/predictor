import pandas as pd
import pytest
from compiler.data.calculation.stats import calculate_feature_ratio, calculate_home_advantage


def test_calculate_feature_ratio_returns_a_calculated_ratio_float_for_feature():
    df = pd.read_csv("/opt/tests/test-data/test-data.csv")
    row = pd.read_csv("/opt/tests/test-data/test-fixture.csv")

    home_shot_ratio = calculate_feature_ratio(
        df=df,
        row=row.iloc[0, :],
        home_away='homeTeam',
        feature='homeShotTargetRatio',
        rating='awayDefenceStrength',
        factor=50,
        row_count=3
    )

    away_shot_ratio = calculate_feature_ratio(
        df=df,
        row=row.iloc[0, :],
        home_away='awayTeam',
        feature='awayShotTargetRatio',
        rating='homeDefenceStrength',
        factor=50,
        row_count=3
    )

    home_save_ratio = calculate_feature_ratio(
        df=df,
        row=row.iloc[0, :],
        home_away='homeTeam',
        feature='homeShotSaveRatio',
        rating='awayAttackStrength',
        factor=50,
        row_count=3
    )

    away_save_ratio = calculate_feature_ratio(
        df=df,
        row=row.iloc[0, :],
        home_away='awayTeam',
        feature='awayShotSaveRatio',
        rating='homeAttackStrength',
        factor=50,
        row_count=3
    )

    assert home_shot_ratio == 0.43
    assert away_shot_ratio == 0.43
    assert home_save_ratio == 0.61
    assert away_save_ratio == 0.85


def test_calculate_home_advantage_returns_a_float():
    df = pd.read_csv("/opt/tests/test-data/test-data.csv")
    row = pd.read_csv("/opt/tests/test-data/test-fixture.csv")

    assert calculate_home_advantage(row=row.iloc[0, :], df=df, index=1179) == 3.0
