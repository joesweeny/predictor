from typing import Optional, List
from datetime import datetime
from predictor.grpc.proto.result.result_pb2 import MatchStats, Result


HOME_SCORE = 'home_score'
AWAY_SCORE = 'away_score'


def TotalGoalsForMatch(stats: MatchStats) -> Optional[int]:
    """
    Calculate the combined home and away goals for a given MatchStats data set
    """
    has_home_goals = stats.HasField(HOME_SCORE)
    has_away_goals = stats.HasField(AWAY_SCORE)

    if has_home_goals is False or has_away_goals is False:
        return

    home_goals = stats.home_score.value
    away_goals = stats.away_score.value

    return home_goals + away_goals


def DaysBetweenResults(current: Result, previous: Result) -> int:
    """
    Calculate the total days between two Results
    """
    current = datetime.utcfromtimestamp(current.date_time)
    current = current.replace(hour=0, minute=0, second=0, microsecond=0)

    previous = datetime.utcfromtimestamp(previous.date_time)
    previous = previous.replace(hour=0, minute=0, second=0, microsecond=0)

    days = (previous - current).days

    return abs(days)


def AverageGoalsScoredByTeam(results: List[Result], team_id: int) -> float:
    """
    Calculate the average goals scored by a Team for a given set of Results
    """
    goals = []

    for res in results:
        match_data = res.match_data

        if match_data.home_team.id == team_id:
            goals.append(match_data.stats.home_score.value)
        else:
            goals.append(match_data.stats.away_score.value)

    return round(sum(goals) / len(goals), 2)


def AverageGoalsConcededByTeam(results: List[Result], team_id: int) -> float:
    """
    Calculate the average goals conceded by a Team for a given set of Results
    """
    goals = []

    for res in results:
        match_data = res.match_data

        if match_data.home_team.id == team_id:
            goals.append(match_data.stats.away_score.value)
        else:
            goals.append(match_data.stats.home_score.value)

    return round(sum(goals) / len(goals), 2)
