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


def GoalsScoredInMatch(result: Result, team_id: int) -> int:
    """
    Return the number of goals scored by a Team for a given Result
    """
    match_data = result.match_data

    if match_data.home_team.id == team_id:
        goals = match_data.stats.home_score.value
    else:
        goals = match_data.stats.away_score.value

    return goals


def GoalsConcededInMatch(result: Result, team_id: int) -> int:
    """
    Return the number of goals conceded by a Team for a given Result
    """
    match_data = result.match_data

    if match_data.home_team.id == team_id:
        goals = match_data.stats.away_score.value
    else:
        goals = match_data.stats.home_score.value

    return goals


def days_between_results(current_date: datetime, previous: Result) -> int:
    """
    Calculate the total days between two Results
    """
    current = current_date.replace(hour=0, minute=0, second=0, microsecond=0)

    previous = datetime.utcfromtimestamp(previous.date_time)
    previous = previous.replace(hour=0, minute=0, second=0, microsecond=0)

    days = (previous - current).days

    return abs(days)


def average_goals_scored_by_home_team(results: List[Result], team_id: int) -> float:
    """
    Calculate the average goals scored by a Home Team for a given set of Results
    """
    goals = []

    for res in results:
        match_data = res.match_data

        if match_data.home_team.id == team_id:
            goals.append(match_data.stats.home_score.value)

    summed = sum(goals)
    total = len(goals)

    return 0 if summed is 0 else round(summed / total, 2)


def average_goals_conceded_by_home_team(results: List[Result], team_id: int) -> float:
    """
    Calculate the average goals conceded by a Home Team for a given set of Results
    """
    goals = []

    for res in results:
        match_data = res.match_data

        if match_data.home_team.id == team_id:
            goals.append(match_data.stats.away_score.value)

    summed = sum(goals)
    total = len(goals)

    return 0 if summed is 0 else round(summed / total, 2)


def average_goals_scored_by_away_team(results: List[Result], team_id: int) -> float:
    """
    Calculate the average goals scored by an Away Team for a given set of Results
    """
    goals = []

    for res in results:
        match_data = res.match_data

        if match_data.away_team.id == team_id:
            goals.append(match_data.stats.away_score.value)

    summed = sum(goals)
    total = len(goals)

    return 0 if summed is 0 else round(summed / total, 2)


def average_goals_conceded_by_away_team(results: List[Result], team_id: int) -> float:
    """
    Calculate the average goals conceded by an Away Team for a given set of Results
    """
    goals = []

    for res in results:
        match_data = res.match_data

        if match_data.away_team.id == team_id:
            goals.append(match_data.stats.home_score.value)

    summed = sum(goals)
    total = len(goals)

    return 0 if summed is 0 else round(summed / total, 2)


def max_goals_scored_by_home_team(results: List[Result], team_id: int) -> float:
    """
    Calculate the maximum goals scored by a Home Team for a given set of Results
    """
    goals = []

    for res in results:
        match_data = res.match_data

        if match_data.home_team.id == team_id:
            goals.append(match_data.stats.home_score.value)

    return max(goals)


def max_goals_scored_by_away_team(results: List[Result], team_id: int) -> float:
    """
    Calculate the maximum goals scored by a Away Team for a given set of Results
    """
    goals = []

    for res in results:
        match_data = res.match_data

        if match_data.away_team.id == team_id:
            goals.append(match_data.stats.away_score.value)

    return max(goals)


def min_goals_scored_by_home_team(results: List[Result], team_id: int) -> float:
    """
    Calculate the minimum goals scored by a Home Team for a given set of Results
    """
    goals = []

    for res in results:
        match_data = res.match_data

        if match_data.home_team.id == team_id:
            goals.append(match_data.stats.home_score.value)

    return min(goals)


def min_goals_scored_by_away_team(results: List[Result], team_id: int) -> float:
    """
    Calculate the minimum goals scored by a Away Team for a given set of Results
    """
    goals = []

    for res in results:
        match_data = res.match_data

        if match_data.away_team.id == team_id:
            goals.append(match_data.stats.away_score.value)

    return min(goals)


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


def AverageGoalsForResults(results: List[Result]) -> Optional:
    """
    Calculate the average goals scored for a given set of Results
    """
    goals = []

    for res in results:
        goals.append(TotalGoalsForMatch(res.match_data.stats))

    goals = list(filter(None.__ne__, goals))

    if not goals:
        return

    return round(sum(goals) / len(goals), 2)

