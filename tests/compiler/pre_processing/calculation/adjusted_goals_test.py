from compiler.grpc.proto.event_pb2 import CardEvent, GoalEvent
from compiler.preprocessing.calculation.adjusted_goals import calculate_adjusted_goals


def test_calculate_adjusted_goals_returns_total_goals_for_low_scoring_team():
    goals = [
        GoalEvent(team_id=1, minute=52, score='0-0')
    ]

    total = calculate_adjusted_goals(team_id=1, home=True, goals=goals, cards=[])

    assert total == 1


def test_calculate_adjusted_goals_returns_total_goals_for_high_scoring_game_with_goals_scored_before_minute_60():
    goals = [
        GoalEvent(team_id=1, minute=12, score='0-0'),
        GoalEvent(team_id=1, minute=25, score='1-0'),
        GoalEvent(team_id=1, minute=27, score='2-0'),
        GoalEvent(team_id=1, minute=45, score='3-0'),
        GoalEvent(team_id=1, minute=55, score='4-0'),
    ]

    total = calculate_adjusted_goals(team_id=1, home=True, goals=goals, cards=[])

    assert total == 5


def test_calculate_adjusted_goals_returns_total_goals_for_game_where_both_teams_are_scoring_frequent_goals():
    goals = [
        GoalEvent(team_id=1, minute=12, score='0-0'),
        GoalEvent(team_id=2, minute=14, score='1-0'),
        GoalEvent(team_id=1, minute=25, score='1-1'),
        GoalEvent(team_id=1, minute=25, score='2-1'),
        GoalEvent(team_id=2, minute=27, score='3-1'),
        GoalEvent(team_id=2, minute=39, score='3-2'),
        GoalEvent(team_id=1, minute=45, score='3-3'),
        GoalEvent(team_id=1, minute=45, score='4-3'),
    ]

    total = calculate_adjusted_goals(team_id=1, home=True, goals=goals, cards=[])

    assert total == 5


def test_calculate_adjusted_goals_returns_total_goals_reducing_last_two_goals_if_game_is_high_scoring_after_minute_60():
    goals = [
        GoalEvent(team_id=1, minute=12, score='0-0'),
        GoalEvent(team_id=1, minute=25, score='1-0'),
        GoalEvent(team_id=1, minute=27, score='2-0'),
        GoalEvent(team_id=1, minute=71, score='3-0'),
        GoalEvent(team_id=1, minute=85, score='4-0'),
    ]

    total = calculate_adjusted_goals(team_id=1, home=True, goals=goals, cards=[])

    assert total == 4


def test_calculate_adjusted_goals_returns_total_goals_reducing_last_three_goals_if_game_is_high_scoring_after_minute_60():
    goals = [
        GoalEvent(team_id=1, minute=12, score='0-0'),
        GoalEvent(team_id=1, minute=25, score='1-0'),
        GoalEvent(team_id=1, minute=71, score='2-0'),
        GoalEvent(team_id=1, minute=72, score='3-0'),
        GoalEvent(team_id=1, minute=85, score='4-0'),
    ]

    total = calculate_adjusted_goals(team_id=1, home=True, goals=goals, cards=[])

    assert total == 3.5


def test_calculate_adjusted_goals_returns_total_goals_but_does_not_reduce_goal_value_if_scored_before_a_red_card():
    goals = [
        GoalEvent(team_id=1, minute=12, score='0-0'),
        GoalEvent(team_id=1, minute=25, score='1-0'),
    ]

    cards = [
        CardEvent(team_id=2, minute=50, type='redcard')
    ]

    total = calculate_adjusted_goals(team_id=1, home=True, goals=goals, cards=cards)

    assert total == 2


def test_calculate_adjusted_goals_returns_total_goals_reducing_goal_values_for_goals_scored_after_a_red_card():
    goals = [
        GoalEvent(team_id=1, minute=12, score='0-0'),
        GoalEvent(team_id=1, minute=25, score='1-0'),
    ]

    cards = [
        CardEvent(team_id=2, minute=5, type='redcard')
    ]

    total = calculate_adjusted_goals(team_id=1, home=True, goals=goals, cards=cards)

    assert total == 1


def test_calculate_adjusted_goals_returns_total_goals_reducing_goal_value_further_if_goal_scored_in_high_scoring_game_after_a_red_card():
    goals = [
        GoalEvent(team_id=1, minute=12, score='0-0'),
        GoalEvent(team_id=1, minute=25, score='1-0'),
        GoalEvent(team_id=1, minute=61, score='2-0'),
        GoalEvent(team_id=1, minute=65, score='3-0'),
        GoalEvent(team_id=1, minute=75, score='4-0'),
        GoalEvent(team_id=1, minute=89, score='5-0'),
    ]

    cards = [
        CardEvent(team_id=2, minute=15, type='redcard')
    ]

    total = calculate_adjusted_goals(team_id=1, home=True, goals=goals, cards=cards)

    assert total == 2.5
