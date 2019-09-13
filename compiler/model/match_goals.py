from compiler.model.odds import OverUnderGoals
from scipy.stats import poisson
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
import pandas as pd
from typing import Dict, List

HOME_LIST = [
    'homeGoals',
    'homeAdvantage',
    'homeShotTargetRatio',
    'awayShotSaveRatio',
    'homeAvgScored',
    'awayAvgConceded'
]

AWAY_LIST = [
    'awayGoals',
    'awayShotTargetRatio',
    'homeShotSaveRatio',
    'awayAvgScored',
    'homeAvgConceded'
]

HOME_DICT = {
    'homeGoals': 'goals',
    'homeAdvantage': 'home',
    'homeShotTargetRatio': 'shotRatio',
    'awayShotSaveRatio': 'saveRatio',
    'homeAvgScored': 'avgScored',
    'awayAvgConceded': 'avgConceded'
}

AWAY_DICT = {
    'awayGoals': 'goals',
    'awayShotTargetRatio': 'shotRatio',
    'homeShotSaveRatio': 'saveRatio',
    'awayAvgScored': 'avgScored',
    'homeAvgConceded': 'avgConceded'
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

    formula = "goals ~ home + shotRatio + saveRatio + avgScored + avgConceded"

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

    matrix = __get_prediction_matrix(home_avg=home_goals_avg, away_avg=away_goals_avg)

    under, over = __calculate_odds(matrix=matrix)

    return OverUnderGoals(under=under, over=over)


def __get_prediction_matrix(home_avg: List, away_avg: List):
    home_pred = [poisson.pmf(i, home_avg) for i in range(0, MAX_GOALS + 1)]
    away_pred = [poisson.pmf(i, away_avg) for i in range(0, MAX_GOALS + 1)]

    return np.outer(np.array(home_pred), np.array(away_pred))


def __calculate_odds(matrix: np.ndarray) -> (float, float):
    under = np.sum(matrix[:2, :2]) + matrix.item((0, 2)) + matrix.item((2, 0))

    return round((1 / under), 2), round((1 / (1 - under)), 2)


def __create_home_fixture_data(fixture: Dict) -> Dict:
    data = {
        'home': fixture['homeAdvantage'],
        'shotRatio': fixture['homeShotTargetRatio'],
        'saveRatio': fixture['awayShotSaveRatio'],
        'avgScored': fixture['homeAvgScored'],
        'avgConceded': fixture['awayAvgConceded'],
    }

    return data


def __create_away_fixture_data(fixture: Dict) -> Dict:
    data = {
        'home': 0,
        'shotRatio': fixture['awayShotTargetRatio'],
        'saveRatio': fixture['homeShotSaveRatio'],
        'avgScored': fixture['awayAvgScored'],
        'avgConceded': fixture['homeAvgConceded'],
    }

    return data
