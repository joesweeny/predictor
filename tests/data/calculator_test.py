from predictor.grpc.proto.result.result_pb2 import Result
from predictor.data import calculator
from google.protobuf import wrappers_pb2


def test_total_goals_returns_home_and_away_goals_combined():
    result = Result()
    result.match_data.stats.home_score.value = wrappers_pb2.Int32Value(value=5).value
    result.match_data.stats.away_score.value = wrappers_pb2.Int32Value(value=0).value

    assert calculator.TotalGoalsForMatch(result) == 5


def test_total_goals_returns_none_if_both_required_values_are_not_present():
    result = Result()

    assert calculator.TotalGoalsForMatch(result) is None


def test_total_goals_returns_none_if_either_required_value_is_missing():
    result = Result()
    result.match_data.stats.home_score.value = wrappers_pb2.Int32Value(value=5).value

    assert calculator.TotalGoalsForMatch(result) is None


def test_total_goals_can_handle_zero_values():
    result = Result()
    result.match_data.stats.home_score.value = wrappers_pb2.Int32Value(value=0).value
    result.match_data.stats.away_score.value = wrappers_pb2.Int32Value(value=0).value

    assert calculator.TotalGoalsForMatch(result) == 0
