import pandas as pd
import pytest
from compiler.model.match_goals import train_glm_model, get_over_under_odds


def test_train_glm_model_uses_data_frame_to_train_model_and_returns_model():
    df = pd.read_csv("/opt/tests/test-data/test-data.csv")

    model = train_glm_model(features=df)

    assert model.df_resid == 2354
    assert model.df_model == 5
    assert model.scale == 1.0


def test_get_over_under_odds_returns_over_under_odds_object():
    df = pd.read_csv("/opt/tests/test-data/test-data.csv")
    fixture = pd.read_csv("/opt/tests/test-data/test-fixture.csv")

    model = train_glm_model(features=df)

    odds = get_over_under_odds(model=model, fixture=fixture.to_dict('records')[0])

    assert odds.get_under_decimal_odds() == 2.9
    assert odds.get_over_decimal_odds() == 1.53
