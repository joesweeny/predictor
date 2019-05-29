import pytest
from datetime import datetime
from mock import MagicMock, Mock
from predictor.data.aggregator.match_goals import MatchGoals
from predictor.grpc.proto.fixture.fixture_pb2 import Fixture
from predictor.grpc.proto.result import result_pb2
from predictor.grpc.result_client import ResultClient
from predictor.grpc.team_stats_client import TeamStatsClient
from predictor.grpc.proto.stats.team import stats_pb2


def test_for_season_data_frame_columns(match_goals):
    value = match_goals.result_client.get_results_for_season.return_value
    value.__iter__.return_value = iter([])

    df = match_goals.for_season(5, datetime.fromisoformat('2019-04-23T18:15:38+00:00'))

    match_goals.result_client.get_results_for_season.assert_called_with(
        season_id=5,
        date_before='2019-04-23T18:15:38+00:00'
    )

    columns = [
        'matchID',
        'round',
        'date',
        'season',
        'averageGoalsForFixture',
        'homeTeamID',
        'homeTeam',
        'homeDaysSinceLastMatch',
        'homeFormation',
        'homeAvgScoredLast5',
        'homeAvgConcededLast5',
        'homeScoredLastMatch',
        'homeConcededLastMatch',
        'homeShotsTotal',
        'homeShotsOnGoal',
        'homeShotsOffGoal',
        'homeShotsInsideBox',
        'homeShotsOutsideBox',
        'homeAttacksTotal',
        'homeAttacksDangerous',
        'homeGoals',
        'awayTeamID',
        'awayTeam',
        'awayDaysSinceLastMatch',
        'awayFormation',
        'awayAvgScoredLast5',
        'awayAvgConcededLast5',
        'awayScoredLastMatch',
        'awayConcededLastMatch',
        'awayShotsTotal',
        'awayShotsOnGoal',
        'awayShotsOffGoal',
        'awayShotsInsideBox',
        'awayShotsOutsideBox',
        'awayAttacksTotal',
        'awayAttacksDangerous',
        'awayGoals',
    ]

    df_columns = df.columns

    assert (df_columns == columns).all()


def test_for_season_converts_result_object_into_data_frame_row(
    match_goals,
    result,
    home_past_result,
    away_past_result,
    team_stats_response
):
    value = match_goals.result_client.get_results_for_season.return_value
    value.__iter__.return_value = iter([result])

    match_goals.result_client.get_results_for_team.side_effect = [
        [
            home_past_result,
            home_past_result,
            away_past_result,
        ],
        [
            away_past_result,
            away_past_result,
            home_past_result,
        ]
    ]

    match_goals.result_client.get_historical_results_for_fixture.side_effect = [
        [
            home_past_result,
            home_past_result,
            away_past_result,
        ]
    ]

    match_goals.team_stats_client.get_team_stats_for_fixture.return_value = team_stats_response

    df = match_goals.for_season(5, datetime.fromisoformat('2019-04-23T18:15:38+00:00'))

    match_goals.result_client.get_results_for_season.assert_called_with(
        season_id=5,
        date_before='2019-04-23T18:15:38+00:00'
    )

    match_goals.team_stats_client.get_team_stats_for_fixture.assert_called_with(fixture_id=66)

    expected = [
        66,
        '4',
        '2019-04-23T18:15:38',
        '2018/19',
        6.00,
        7901,
        'West Ham United',
        3,
        '4-4-2',
        4.33,
        1.67,
        5,
        2,
        34,
        12,
        22,
        15,
        5,
        None,
        None,
        2,
        496,
        'Tottenham Hotspur',
        5,
        '5-3-1-1',
        1.33,
        3.67,
        1,
        3,
        34,
        12,
        22,
        15,
        5,
        None,
        None,
        2,
    ]

    row = df.iloc[0, :].values.tolist()

    assert row == expected


def test_for_reason_populates_multiple_rows_of_data_for_multiple_results(
        match_goals,
        result,
        home_past_result,
        away_past_result
):
    value = match_goals.result_client.get_results_for_season.return_value
    value.__iter__.return_value = iter([result, result, result])

    match_goals.result_client.get_results_for_team.side_effect = [
        [home_past_result],
        [away_past_result],
        [home_past_result],
        [away_past_result],
        [home_past_result],
        [away_past_result],
        [home_past_result],
        [away_past_result],
        [home_past_result],
        [away_past_result],
        [home_past_result],
    ]

    match_goals.result_client.get_historical_results_for_fixture.side_effect = [
        [
            home_past_result,
            home_past_result,
            away_past_result,
        ],
        [
            home_past_result,
            home_past_result,
            away_past_result,
        ],
        [
            home_past_result,
            home_past_result,
            away_past_result,
        ]
    ]

    df = match_goals.for_season(5, datetime.fromisoformat('2019-04-23T18:15:38+00:00'))

    match_goals.result_client.get_results_for_season.assert_called_with(
        season_id=5,
        date_before='2019-04-23T18:15:38+00:00'
    )

    assert df.shape == (3, 37)


def test_for_fixture_data_frame_columns(
    match_goals,
    fixture,
    home_past_result,
    away_past_result
):
    match_goals.result_client.get_results_for_team.side_effect = [
        [
            home_past_result,
            home_past_result,
            away_past_result,
        ],
        [
            away_past_result,
            away_past_result,
            home_past_result,
        ]
    ]

    match_goals.result_client.get_historical_results_for_fixture.side_effect = [
        [
            home_past_result,
            home_past_result,
            away_past_result,
        ]
    ]

    df = match_goals.for_fixture(fixture=fixture)

    columns = [
        'matchID',
        'round',
        'date',
        'season',
        'averageGoalsForFixture',
        'homeTeamID',
        'homeTeam',
        'homeDaysSinceLastMatch',
        'homeFormation',
        'homeAvgScoredLast5',
        'homeAvgConcededLast5',
        'homeScoredLastMatch',
        'homeConcededLastMatch',
        'homeShotsTotal',
        'homeShotsOnGoal',
        'homeShotsOffGoal',
        'homeShotsInsideBox',
        'homeShotsOutsideBox',
        'homeAttacksTotal',
        'homeAttacksDangerous',
        'homeGoals',
        'awayTeamID',
        'awayTeam',
        'awayDaysSinceLastMatch',
        'awayFormation',
        'awayAvgScoredLast5',
        'awayAvgConcededLast5',
        'awayScoredLastMatch',
        'awayConcededLastMatch',
        'awayShotsTotal',
        'awayShotsOnGoal',
        'awayShotsOffGoal',
        'awayShotsInsideBox',
        'awayShotsOutsideBox',
        'awayAttacksTotal',
        'awayAttacksDangerous',
        'awayGoals',
    ]

    df_columns = df.columns

    assert (df_columns == columns).all()
    assert df.shape == (1, 37)


def test_for_fixture_returns_dataframe_of_collated_fixture_data(
    match_goals,
    fixture,
    home_past_result,
    away_past_result
):
    match_goals.result_client.get_results_for_team.side_effect = [
        [
            home_past_result,
            home_past_result,
            away_past_result,
        ],
        [
            away_past_result,
            away_past_result,
            home_past_result,
        ]
    ]

    match_goals.result_client.get_historical_results_for_fixture.side_effect = [
        [
            home_past_result,
            home_past_result,
            away_past_result,
        ]
    ]

    df = match_goals.for_fixture(fixture=fixture)

    row = df.iloc[0, :]

    assert row['matchID'] == 66
    assert row['round'] == '4'
    assert row['date'] == '2019-04-23T18:15:38'
    assert row['season'] == '2018/19'
    assert row['averageGoalsForFixture'] == 6.00
    assert row['homeTeamID'] == 7901
    assert row['homeTeam'] == 'West Ham United'
    assert row['homeDaysSinceLastMatch'] == 3
    assert row['homeAvgScoredLast5'] == 4.33
    assert row['homeAvgConcededLast5'] == 1.67
    assert row['homeScoredLastMatch'] == 5
    assert row['homeConcededLastMatch'] == 2
    assert row['awayTeamID'] == 496
    assert row['awayTeam'] == 'Tottenham Hotspur'
    assert row['awayDaysSinceLastMatch'] == 5
    assert row['awayAvgScoredLast5'] == 1.33
    assert row['awayAvgConcededLast5'] == 3.67
    assert row['awayScoredLastMatch'] == 1
    assert row['awayConcededLastMatch'] == 3


@pytest.fixture()
def match_goals():
    result_client = MagicMock(spec=ResultClient)
    team_stats_client = Mock(spec=TeamStatsClient)
    return MatchGoals(result_client, team_stats_client)


@pytest.fixture()
def result():
    result = result_pb2.Result()
    result.id = 66

    result.competition.id = 55
    result.competition.is_cup.value = False

    result.season.name = '2018/19'

    result.round.name = '4'

    result.season.id = 39910
    result.season.is_current.value = True

    result.date_time = 1556043338

    result.match_data.home_team.id = 7901
    result.match_data.home_team.name = 'West Ham United'
    result.match_data.away_team.id = 496
    result.match_data.away_team.name = 'Tottenham Hotspur'
    result.match_data.stats.home_formation.value = '4-4-2'
    result.match_data.stats.away_formation.value = '5-3-1-1'
    result.match_data.stats.home_score.value = 2
    result.match_data.stats.away_score.value = 2

    return result


@pytest.fixture()
def home_past_result():
    result = result_pb2.Result()
    result.date_time = 1555761600
    result.match_data.home_team.id = 7901
    result.match_data.home_team.name = 'West Ham United'
    result.match_data.away_team.id = 496
    result.match_data.away_team.name = 'Tottenham Hotspur'
    result.match_data.stats.home_score.value = 5
    result.match_data.stats.away_score.value = 2
    return result


@pytest.fixture()
def away_past_result():
    result = result_pb2.Result()
    result.date_time = 1555549200
    result.match_data.home_team.id = 496
    result.match_data.home_team.name = 'Manchester City'
    result.match_data.away_team.id = 7901
    result.match_data.away_team.name = 'Liverpool'
    result.match_data.stats.home_score.value = 1
    result.match_data.stats.away_score.value = 3
    return result


@pytest.fixture
def team_stats_response():
    response = stats_pb2.StatsResponse()

    response.home_team.shots_total.value = 34
    response.home_team.shots_on_goal.value = 12
    response.home_team.shots_off_goal.value = 22
    response.home_team.shots_inside_box.value = 15
    response.home_team.shots_outside_box.value = 5

    response.away_team.shots_total.value = 34
    response.away_team.shots_on_goal.value = 12
    response.away_team.shots_off_goal.value = 22
    response.away_team.shots_inside_box.value = 15
    response.away_team.shots_outside_box.value = 5

    return response


@pytest.fixture()
def fixture():
    fixture = Fixture()
    fixture.id = 66

    fixture.competition.id = 55
    fixture.competition.is_cup.value = False

    fixture.season.name = '2018/19'

    fixture.round.name = '4'

    fixture.season.id = 39910
    fixture.season.is_current.value = True

    fixture.date_time = 1556043338

    fixture.home_team.id = 7901
    fixture.home_team.name = 'West Ham United'
    fixture.away_team.id = 496
    fixture.away_team.name = 'Tottenham Hotspur'

    return fixture
