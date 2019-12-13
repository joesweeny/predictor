from typing import List
import numpy as np
from scipy.stats import poisson

MAX_GOALS = 5


def get_prediction_matrix(home_avg: List, away_avg: List):
    home_pred = [poisson.pmf(i, home_avg) for i in range(0, MAX_GOALS + 1)]
    away_pred = [poisson.pmf(i, away_avg) for i in range(0, MAX_GOALS + 1)]

    return np.outer(np.array(home_pred), np.array(away_pred))


def calculate_odds(matrix: np.ndarray) -> (float, float):
    under = np.sum(matrix[:2, :2]) + matrix.item((0, 2)) + matrix.item((2, 0))

    return round((1 / under), 2), round((1 / (1 - under)), 2)
