from typing import List


def calculate_team_ratings(
    k_factor: int,
    home_team: float,
    away_team: float,
    home_goals: int,
    away_goals: int
) -> List[float]:
    """
    Calculate new ELO ratings for home and away teams based on result
    :param k_factor: int
    :param home_team: float
    :param away_team: float
    :param home_goals: int
    :param away_goals: int
    :return: List
    """
    prob_win_home = 1 / (1 + 10 ** ((away_team - home_team) / 400))
    prob_win_away = 1 - prob_win_home

    result = 0

    if home_goals > away_goals:
        result = 2
    elif home_goals < away_goals:
        result = 1

    if result == 2:
        new_home_elo = home_team + k_factor * (1 - prob_win_home)
        new_away_elo = away_team + k_factor * (0 - prob_win_away)
    elif result == 1:
        new_home_elo = home_team + k_factor * (0 - prob_win_home)
        new_away_elo = away_team + k_factor * (1 - prob_win_away)
    else:
        new_home_elo = home_team + k_factor * (0.5 - prob_win_home)
        new_away_elo = away_team + k_factor * (0.5 - prob_win_away)

    return [round(new_home_elo, 2), round(new_away_elo, 2)]
