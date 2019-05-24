import pytest
from datetime import datetime
from predictor.grpc.proto.result.result_pb2 import MatchStats, Result
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


def test_days_between_results_returns_total_days_between_two_results():
    last = Result()
    last.date_time = 1556209112

    current = datetime.utcfromtimestamp(1555891200)

    days = calculator.days_between_results(current, last)

    assert days == 3


def test_days_between_results_casts_negative_days_to_positive():
    last = Result()
    last.date_time = 1555891200

    current = datetime.utcfromtimestamp(1556209112)

    days = calculator.days_between_results(current, last)

    assert days == 3


def test_average_goals_scored_by_team_returns_float(home_result, away_result):
    results = [
        home_result,
        home_result,
        home_result,
        away_result,
        home_result,
        away_result,
        away_result,
        away_result,
        home_result,
    ]

    assert calculator.AverageGoalsScoredByTeam(results, 7901) == 1.56
    assert calculator.AverageGoalsScoredByTeam(results, 496) == 1.33


def test_average_goals_conceded_by_team_returns_float(home_result, away_result):
    results = [
        home_result,
        home_result,
        home_result,
        away_result,
        home_result,
        away_result,
        away_result,
        away_result,
        home_result,
    ]

    assert calculator.AverageGoalsConcededByTeam(results, 7901) == 1.33
    assert calculator.AverageGoalsConcededByTeam(results, 496) == 1.56


def test_average_goals_for_results_returns_float(home_result, away_result):
    results = [
        home_result,
        away_result,
        home_result,
    ]

    assert calculator.AverageGoalsForResults(results) == 2.67


def test_average_goals_for_results_can_handle_results_without_goals_set(home_result):
    results = [
        home_result,
        home_result,
        Result(),
    ]

    assert calculator.AverageGoalsForResults(results) == 2.00


def test_average_goals_for_results_can_handle_games_where_goals_are_zero():
    result = Result()
    result.match_data.stats.home_score.value = 0
    result.match_data.stats.away_score.value = 0

    results = [
        result,
        result,
        result,
    ]

    assert calculator.AverageGoalsForResults(results) == 0.00


def test_average_goals_for_results_can_handle_results_can_do_not_contain_goals():
    assert calculator.AverageGoalsForResults([Result()]) is None


def test_goals_scored_in_match_returns_int(home_result):
    assert calculator.GoalsScoredInMatch(home_result, 7901) == 2
    assert calculator.GoalsScoredInMatch(home_result, 496) == 0


def test_goals_conceded_in_match_returns_int(away_result):
    assert calculator.GoalsConcededInMatch(away_result, 7901) == 3
    assert calculator.GoalsConcededInMatch(away_result, 496) == 1


@pytest.fixture()
def home_result():
    result = Result()
    result.match_data.home_team.id = 7901
    result.match_data.away_team.id = 496
    result.match_data.stats.home_score.value = 2
    result.match_data.stats.away_score.value = 0

    return result


@pytest.fixture()
def away_result():
    result = Result()
    result.match_data.home_team.id = 496
    result.match_data.away_team.id = 7901
    result.match_data.stats.home_score.value = 3
    result.match_data.stats.away_score.value = 1

    return result
