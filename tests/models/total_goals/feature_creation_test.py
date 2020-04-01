import pandas as pd
import pytest
from compiler.models.total_goals import feature_creation


def test_calculate_round_goal_stats_returns_a_dictionary_containing_dictionary_key_for_each_season():
    df = pd.read_csv("/opt/tests/test-data/premier-league-2014-2020.csv")
    stats = feature_creation.calculate_round_goal_stats(df)

    seasons = df['season'].unique().tolist()

    for season in seasons:
        assert season in stats
    assert len(seasons) == len(stats.keys())


def test_calculate_round_goal_stats_orders_round_stats_in_order_from_highest_to_lowest_goals():
    df = pd.read_csv("/opt/tests/test-data/premier-league-2014-2020.csv")
    stats = feature_creation.calculate_round_goal_stats(df)

    table = stats['2019/2020'][1]

    counter = 0
    for team, goals in table.items():
        if counter == 0:
            counter = goals

        assert counter >= goals
        counter += goals


def test_calculate_round_goal_stats_correctly_calculates_a_running_total_of_total_goals_for_each_team():
    df = pd.read_csv("/opt/tests/test-data/premier-league-2014-2020.csv")
    stats = feature_creation.calculate_round_goal_stats(df)

    table = stats['2019/2020'][1]

    assert table['Liverpool'] == 5
    assert table['Norwich City'] == 5
    assert table['West Ham United'] == 5
    assert table['Manchester City'] == 5
    assert table['Tottenham Hotspur'] == 4
    assert table['Aston Villa'] == 4
    assert table['Manchester United'] == 4
    assert table['Chelsea'] == 4
    assert table['Watford'] == 3
    assert table['Brighton & Hove Albion'] == 3
    assert table['Burnley'] == 3
    assert table['Southampton'] == 3
    assert table['AFC Bournemouth'] == 2
    assert table['Sheffield United'] == 2
    assert table['Newcastle United'] == 1
    assert table['Arsenal'] == 1
    assert table['Crystal Palace'] == 0
    assert table['Everton'] == 0
    assert table['Leicester City'] == 0
    assert table['Wolverhampton Wanderers'] == 0


def test_calculate_round_goal_stats_raises_key_error_if_unable_to_find_a_teams_previous_total():
    data = [
        {
            "season": "2019/2020",
            "round": 1,
            "homeTeam": "West Ham United",
            "awayTeam": "Chelsea",
            "totalGoals": 4,
        },
        {
            "season": "2019/2020",
            "round": 4,
            "homeTeam": "West Ham United",
            "awayTeam": "Arsenal",
            "totalGoals": 2,
        },
    ]

    df = pd.DataFrame(data)

    with pytest.raises(KeyError):
        feature_creation.calculate_round_goal_stats(df)


def test_convert_to_league_positions_converts_a_dictionary_of_goal_stats_into_league_table_dictionary():
    stats = {
        '2019/2020': {
            1: {
                'Chelsea': 25,
                'West Ham United': 23,
                'Arsenal': 22,
            },
            2: {
                'West Ham United': 28,
                'Chelsea': 26,
                'Arsenal': 24,
            }
        }
    }

    tables = feature_creation.convert_to_league_positions(stats)

    print(tables)

    expected = {
        '2019/2020': {
            2: [
                {
                    'team': 'Chelsea',
                    'position': 1,
                    'goals': 25,
                    'diff': 0,
                },
                {
                    'team': 'West Ham United',
                    'position': 2,
                    'goals': 23,
                    'diff': 0,
                },
                {
                    'team': 'Arsenal',
                    'position': 3,
                    'goals': 22,
                    'diff': 0,
                }
            ],
            3: [
                {
                    'team': 'West Ham United',
                    'position': 1,
                    'goals': 28,
                    'diff': 1,
                },
                {
                    'team': 'Chelsea',
                    'position': 2,
                    'goals': 26,
                    'diff': 1,
                },
                {
                    'team': 'Arsenal',
                    'position': 3,
                    'goals': 24,
                    'diff': 0,
                }
            ],
        }
    }

    assert tables == expected
