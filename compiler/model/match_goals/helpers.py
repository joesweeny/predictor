from typing import List
import numpy as np
from scipy.stats import poisson

MAX_GOALS = 5

MARKET_NOT_SUPPORTED = "market not supported"


def get_prediction_matrix(home_avg: List, away_avg: List):
    home_pred = [poisson.pmf(i, home_avg) for i in range(0, MAX_GOALS + 1)]
    away_pred = [poisson.pmf(i, away_avg) for i in range(0, MAX_GOALS + 1)]

    return np.outer(np.array(home_pred), np.array(away_pred))


def calculate_odds(matrix: np.ndarray, market: str) -> (float, float):
    switcher = {
        "over_under_15": over_under_15,
        "over_under_25": over_under_25,
        "over_under_35": over_under_35,
    }

    func = switcher.get(market.lower(), MARKET_NOT_SUPPORTED)

    if func == MARKET_NOT_SUPPORTED:
        raise Exception(MARKET_NOT_SUPPORTED)

    under = func(matrix)

    return round((1 / under), 2), round((1 / (1 - under)), 2)


def over_under_15(matrix: np.ndarray):
    return np.sum(matrix[:1, :2]) + matrix.item((0, 2)) + matrix.item((1, 0))


def over_under_25(matrix: np.ndarray):
    return np.sum(matrix[:2, :2]) + matrix.item((0, 2)) + matrix.item((2, 0))


def over_under_35(matrix: np.ndarray):
    return np.sum(matrix[:3, :3]) + matrix.item((0, 3)) + matrix.item((3, 0))
