import numpy as np
import pandas as pd
from typing import Dict


def calculate_round_goal_stats(fixtures: pd.DataFrame) -> Dict:
    """
    Calculate rolling goal scoring stats for each season, round and team within dataframe
    Each round is ordered by the team scoring the most goals across a season

    :param fixtures
    :return Dict
    :raises KeyError
    """
    seasons = fixtures['season'].unique()
    rounds = np.sort(fixtures['round'].unique())

    stats = {}

    for season in seasons:
        stats[season] = {}
        season_rows = fixtures[fixtures['season'] == season]

        for r in rounds:
            round_stats = {}
            round_rows = season_rows[season_rows['round'] == r]

            if len(round_rows) == 0:
                continue

            for index, row in round_rows.iterrows():
                round_stats[row['homeTeam']] = __get_previous_round_goals(
                    stats[season],
                    row['homeTeam'],
                    r,
                    row['totalGoals']
                )
                round_stats[row['awayTeam']] = __get_previous_round_goals(
                    stats[season],
                    row['awayTeam'],
                    r,
                    row['totalGoals']
                )

            stats[season][r] = dict(sorted(round_stats.items(), key=lambda x: x[1], reverse=True))

    return stats


def __get_previous_round_goals(stats: Dict, team: str, r: int, goals: int):
    if r == 1:
        return goals

    one_round_previous = stats[r - 1]

    if team in one_round_previous:
        return one_round_previous[team] + goals

    two_rounds_previous = stats[r - 2]

    if team in two_rounds_previous:
        return two_rounds_previous[team] + goals

    raise KeyError("Key " + team + " not found when creating round stats for round " + str(r))
