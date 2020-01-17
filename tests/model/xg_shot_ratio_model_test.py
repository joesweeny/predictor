import pandas as pd
import pytest
from compiler.model.match_goals.xg_shot_ratio import train_glm_model, get_over_under_odds


def test_train_glm_model_uses_data_frame_to_train_model_and_returns_model():
    df = pd.read_csv("/opt/tests/test-data/test-data.csv")

    model = train_glm_model(features=df)

    assert model.df_resid == 2353
    assert model.df_model == 6
    assert model.scale == 1.0


def test_get_over_under_odds_returns_odds_for_1_5_goals_market():
    df = pd.read_csv("/opt/tests/test-data/test-data.csv")
    fixture = pd.read_csv("/opt/tests/test-data/test-fixture.csv")

    model = train_glm_model(features=df)

    odds = get_over_under_odds(model=model, fixture=fixture.to_dict('records')[0], market="OVER_UNDER_15")

    assert odds[0].get_price() == 5.82
    assert odds[0].get_selection() == "UNDER"
    assert odds[1].get_price() == 1.21
    assert odds[1].get_selection() == "OVER"


def test_get_over_under_odds_returns_odds_for_2_5_goals_market():
    df = pd.read_csv("/opt/tests/test-data/test-data.csv")
    fixture = pd.read_csv("/opt/tests/test-data/test-fixture.csv")

    model = train_glm_model(features=df)

    odds = get_over_under_odds(model=model, fixture=fixture.to_dict('records')[0], market="OVER_UNDER_25")

    assert odds[0].get_price() == 3.12
    assert odds[0].get_selection() == "UNDER"
    assert odds[1].get_price() == 1.47
    assert odds[1].get_selection() == "OVER"


def test_get_over_under_odds_returns_odds_for_3_5_goals_market():
    df = pd.read_csv("/opt/tests/test-data/test-data.csv")
    fixture = pd.read_csv("/opt/tests/test-data/test-fixture.csv")

    model = train_glm_model(features=df)

    odds = get_over_under_odds(model=model, fixture=fixture.to_dict('records')[0], market="OVER_UNDER_35")

    assert odds[0].get_price() == 1.65
    assert odds[0].get_selection() == "UNDER"
    assert odds[1].get_price() == 2.53
    assert odds[1].get_selection() == "OVER"


def test_get_over_under_odds_raises_exception_if_market_is_not_supported():
    df = pd.read_csv("/opt/tests/test-data/test-data.csv")
    fixture = pd.read_csv("/opt/tests/test-data/test-fixture.csv")

    model = train_glm_model(features=df)

    with pytest.raises(Exception):
        get_over_under_odds(model=model, fixture=fixture.to_dict('records')[0], market="OVER_UNDER_95")
