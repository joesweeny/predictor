from typing import Optional
from datetime import datetime
from predictor.grpc.proto.result.result_pb2 import MatchStats, Result
from predictor.grpc.proto.fixture.fixture_pb2 import Fixture


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


def DaysBetweenResults(recent: Result, previous: Result) -> int:
    """
    Calculate the total days between two Results
    """
    last = datetime.utcfromtimestamp(previous.date_time)
    last = last.replace(hour=0, minute=0, second=0, microsecond=0)
    current = datetime.utcfromtimestamp(recent.date_time)
    current = current.replace(hour=0, minute=0, second=0, microsecond=0)

    days = (last - current).days

    return abs(days)
