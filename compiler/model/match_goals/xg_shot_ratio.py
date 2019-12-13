from compiler.model.odds import OverUnderGoals
from compiler.model.match_goals.helpers import get_prediction_matrix, calculate_odds
import statsmodels.api as sm
import statsmodels.formula.api as smf
import pandas as pd
from typing import Dict

HOME_LIST = [
    'homeGoals',
    'homeAdvantage',
    'homeAttackStrength',
    'homeXGFor',
    'awayXGAgainst',
    'homeAvgScored',
    'awayAvgConceded',
    'homeShotTargetRatio',
    'awayShotSaveRatio'
]

AWAY_LIST = [
    'awayGoals',
    'awayAttackStrength',
    'awayXGFor',
    'homeXGAgainst',
    'awayAvgScored',
    'homeAvgConceded',
    'awayShotTargetRatio',
    'homeShotSaveRatio'
]

HOME_DICT = {
    'homeGoals': 'goals',
    'homeAdvantage': 'home',
    'homeAttackStrength': 'attackStrength',
    'homeAvgScored': 'avgScored',
    'awayAvgConceded': 'avgConceded',
    'homeXGFor': 'xGFor',
    'awayXGAgainst': 'xGAgainst',
    'homeShotTargetRatio': 'shotRatio',
    'awayShotSaveRatio': 'saveRatio',
}

AWAY_DICT = {
    'awayGoals': 'goals',
    'awayAttackStrength': 'attackStrength',
    'awayAvgScored': 'avgScored',
    'homeAvgConceded': 'avgConceded',
    'awayXGFor': 'xGFor',
    'homeXGAgainst': 'xGAgainst',
    'awayShotTargetRatio': 'shotRatio',
    'homeShotSaveRatio': 'saveRatio',
}

MAX_GOALS = 5


def train_glm_model(features: pd.DataFrame) -> smf.glm:
    """
    Train and return a StatsModels GLM model using the dataframe provided as the
    only argument
    :param features:
    :return: smf.glm
    """
    home_data = features[HOME_LIST].rename(columns=HOME_DICT)
    away_data = features[AWAY_LIST].assign(home=0).rename(columns=AWAY_DICT)

    data = pd.concat([home_data, away_data], sort=False, ignore_index=False)

    formula = "goals ~ home + attackStrength + avgScored + avgConceded + xGFor + xGAgainst + shotRatio + saveRatio"

    model = smf.glm(formula=formula, data=data, family=sm.families.Poisson()).fit()

    return model


def get_over_under_odds(model: smf.glm, fixture: Dict) -> OverUnderGoals:
    """
    Use trained GLM model to make prediction and return calculated decimal odds
    :param model:
    :param fixture:
    :return: OverUnderGoals
    """
    home_data = pd.DataFrame(data=__create_home_fixture_data(fixture=fixture), index=[1])
    away_data = pd.DataFrame(data=__create_away_fixture_data(fixture=fixture), index=[1])

    home_goals_avg = model.predict(home_data).values[0]
    away_goals_avg = model.predict(away_data).values[0]

    matrix = get_prediction_matrix(home_avg=home_goals_avg, away_avg=away_goals_avg)

    under, over = calculate_odds(matrix=matrix)

    return OverUnderGoals(model='xg_shot_ratio', under=under, over=over)


def __create_home_fixture_data(fixture: Dict) -> Dict:
    data = {
        'home': fixture['homeAdvantage'],
        'attackStrength': fixture['homeAttackStrength'],
        'avgScored': fixture['homeAvgScored'],
        'avgConceded': fixture['awayAvgConceded'],
        'xGFor': fixture['homeXGFor'],
        'xGAgainst': fixture['awayXGAgainst'],
        'shotRatio': fixture['homeShotTargetRatio'],
        'saveRatio': fixture['awayShotSaveRatio'],
    }

    return data


def __create_away_fixture_data(fixture: Dict) -> Dict:
    data = {
        'home': 0,
        'attackStrength': fixture['awayAttackStrength'],
        'avgScored': fixture['awayAvgScored'],
        'avgConceded': fixture['homeAvgConceded'],
        'xGFor': fixture['awayXGFor'],
        'xGAgainst': fixture['homeXGAgainst'],
        'shotRatio': fixture['awayShotTargetRatio'],
        'saveRatio': fixture['homeShotSaveRatio'],
    }

    return data
