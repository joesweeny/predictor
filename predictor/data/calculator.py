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


def DaysSinceLastMatch(current_match: Fixture, last_match: Result) -> int:
    """
    Calculate the total days between a Fixture and a previous Result
    """
    last = datetime.utcfromtimestamp(last_match.date_time)
    last = last.replace(hour=0, minute=0, second=0, microsecond=0)
    current = datetime.utcfromtimestamp(current_match.date_time)
    current = current.replace(hour=0, minute=0, second=0, microsecond=0)

    return (last - current).days
