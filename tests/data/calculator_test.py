from predictor.grpc.proto.result.result_pb2 import MatchStats
from predictor.data import calculator


def test_total_goals_returns_home_and_away_goals_combined():
    stats = MatchStats()
    stats.home_score.value = 5
    stats.away_score.value = 0

    assert calculator.TotalGoalsForMatch(stats) == 5


def test_total_goals_returns_none_if_both_required_values_are_not_present():
    stats = MatchStats()

    assert calculator.TotalGoalsForMatch(stats) is None


def test_total_goals_returns_none_if_either_required_value_is_missing():
    stats = MatchStats()
    stats.home_score.value = 5

    assert calculator.TotalGoalsForMatch(stats) is None


def test_total_goals_can_handle_zero_values():
    stats = MatchStats()
    stats.home_score.value = 0
    stats.away_score.value = 0

    assert calculator.TotalGoalsForMatch(stats) == 0
