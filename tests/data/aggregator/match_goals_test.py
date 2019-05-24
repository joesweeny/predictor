import pytest
from mock import MagicMock, Mock
from predictor.data.aggregator.match_goals import MatchGoals
from predictor.grpc.fixture_client import FixtureClient
from predictor.grpc.proto.fixture.fixture_pb2 import Fixture
from predictor.grpc.proto.result import result_pb2
from predictor.grpc.result_client import ResultClient
from predictor.grpc.team_stats_client import TeamStatsClient
from predictor.grpc.proto.stats.team import stats_pb2


def test_for_season_data_frame_columns(mock_result_client, match_goals):
    value = mock_result_client.get_results_for_season.return_value
    value.__iter__.return_value = iter([])

    df = match_goals.for_season(5, '2019-04-23T18:15:38+00:00')

    mock_result_client.get_results_for_season.assert_called_with(
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
        mock_result_client,
        mock_team_stats_client,
        match_goals,
        result,
        home_past_result,
        away_past_result,
        team_stats_response
):
    value = mock_result_client.get_results_for_season.return_value
    value.__iter__.return_value = iter([result])

    mock_result_client.get_results_for_team.side_effect = [
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

    mock_result_client.get_historical_results_for_fixture.side_effect = [
        [
            home_past_result,
            home_past_result,
            away_past_result,
        ]
    ]

    mock_team_stats_client.get_team_stats_for_fixture.return_value = team_stats_response

    df = match_goals.for_season(5, '2019-04-23T18:15:38+00:00')

    mock_result_client.get_results_for_season.assert_called_with(
        season_id=5,
        date_before='2019-04-23T18:15:38+00:00'
    )

    mock_team_stats_client.get_team_stats_for_fixture.assert_called_with(fixture_id=66)

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
        mock_result_client,
        match_goals,
        result,
        home_past_result,
        away_past_result
):
    value = mock_result_client.get_results_for_season.return_value
    value.__iter__.return_value = iter([result, result, result])

    mock_result_client.get_results_for_team.side_effect = [
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

    mock_result_client.get_historical_results_for_fixture.side_effect = [
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

    df = match_goals.for_season(5, '2019-04-23T18:15:38+00:00')

    mock_result_client.get_results_for_season.assert_called_with(
        season_id=5,
        date_before='2019-04-23T18:15:38+00:00'
    )

    assert df.shape == (3, 37)


def test_for_fixture_data_frame_columns(mock_fixture_client, match_goals, fixture):
    mock_fixture_client.get_fixture_by_id.return_value = fixture

    df = match_goals.for_fixture(66)

    mock_fixture_client.get_fixture_by_id.assert_called_with(fixture_id=66)

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


@pytest.fixture
def mock_fixture_client():
    return Mock(spec=FixtureClient)


@pytest.fixture
def mock_result_client():
    return MagicMock(spec=ResultClient)


@pytest.fixture
def mock_team_stats_client():
    return Mock(spec=TeamStatsClient)


@pytest.fixture()
def match_goals(mock_fixture_client, mock_result_client, mock_team_stats_client):
    return MatchGoals(mock_fixture_client, mock_result_client, mock_team_stats_client)


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
    result = Fixture()
    result.id = 66

    result.competition.id = 55
    result.competition.is_cup.value = False

    result.season.name = '2018/19'

    result.round.name = '4'

    result.season.id = 39910
    result.season.is_current.value = True

    result.date_time = 1556043338

    result.home_team.id = 7901
    result.home_team.name = 'West Ham United'
    result.away_team.id = 496
    result.away_team.name = 'Tottenham Hotspur'

    return result
