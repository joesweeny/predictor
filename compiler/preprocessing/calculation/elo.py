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
    prob_home_win = 1 / (10 ** ((away_team - home_team) / 400) + 1)
    prob_away_win = 1 - prob_home_win

    result = 0

    if home_goals > away_goals:
        result = 2
    elif home_goals < away_goals:
        result = 1

    if result == 2:
        home_team += k_factor * (1 - prob_home_win)
        away_team += k_factor * (0 - prob_away_win)
    elif result == 1:
        home_team += k_factor * (0 - prob_home_win)
        away_team += k_factor * (1 - prob_away_win)
    else:
        home_team += k_factor * (0.5 - prob_home_win)
        away_team += k_factor * (0.5 - prob_away_win)

    return [round(home_team, 2), round(away_team, 2)]


def calculate_attack_and_defence_ratings(k_factor: int, attack: float, defence: float, goals: int) -> List[float]:
    """
    Calculate new ELO attack and defence ratings based on goals scored by an attacking team
    :param k_factor: int
    :param attack:  float
    :param defence: float
    :param goals: int
    :return: List[float]
    """
    prob_no_goal = 1 / (10 ** ((defence - attack) / 400) + 1)
    prob_goal_scored = 1 - prob_no_goal

    if goals == 0:
        attack -= k_factor * prob_no_goal
        defence += k_factor * prob_no_goal
    else:
        attack += (k_factor * goals) * prob_goal_scored
        defence -= (k_factor * goals) * prob_goal_scored

    return [round(attack, 2), round(defence, 2)]
