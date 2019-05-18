import pytest
from mock import MagicMock, Mock
from predictor.data.aggregator.match_goals import MatchGoals
from predictor.grpc.proto.result import result_pb2
from predictor.grpc.result_client import ResultClient
from predictor.grpc.team_stats_client import TeamStatsClient
from predictor.grpc.proto.stats.team import stats_pb2


def test_for_season_dataframe_columns(mock_result_client, match_goals):
    value = mock_result_client.GetResultsForSeason.return_value
    value.__iter__.return_value = iter([])

    df = match_goals.for_season(5)

    mock_result_client.GetResultsForSeason.assert_called_with(5)

    columns = [
        'Match ID',
        'Round',
        'Referee ID',
        'Venue ID',
        'Date',
        'Average Goals for Fixture',
        'Home Team ID',
        'Home Team Name',
        'Home Days Since Last Match',
        'Home Formation',
        'Home Avg Goals Scored Last 5',
        'Home Avg Goals Conceded Last 5',
        'Home Goals Scored Last Match',
        'Home Goals Conceded Last Match',
        'Home Shots Total',
        'Home Shots On Goal',
        'Home Shots Off Goal',
        'Home Shots Inside Box',
        'Home Shots Outside Box',
        'Home Attacks Total',
        'Home Attacks Dangerous',
        'Home Corners',
        'Home Possession',
        'Home Pass Total',
        'Home Pass Accuracy',
        'Home Pass Percentage',
        'Away Team ID',
        'Away Team Name',
        'Away Days Since Last Match',
        'Away Formation',
        'Away Avg Goals Scored Last 5',
        'Away Avg Goals Conceded Last 5',
        'Away Goals Scored Last Match',
        'Away Goals Conceded Last Match',
        'Away Shots Total',
        'Away Shots On Goal',
        'Away Shots Off Goal',
        'Away Shots Inside Box',
        'Away Shots Outside Box',
        'Away Attacks Total',
        'Away Attacks Dangerous',
        'Away Corners',
        'Away Possession',
        'Away Pass Total',
        'Away Pass Accuracy',
        'Away Pass Percentage',
        'Total Goals in Match',
    ]

    df_columns = df.columns

    assert (df_columns == columns).all()


def test_for_season_converts_result_object_into_dataframe_row(
        mock_result_client,
        mock_team_stats_client,
        match_goals,
        result,
        home_past_result,
        away_past_result,
        team_stats_response
):
    value = mock_result_client.GetResultsForSeason.return_value
    value.__iter__.return_value = iter([result])

    mock_result_client.GetResultsForTeam.side_effect = [
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

    mock_result_client.GetHistoricalResultsForFixture.side_effect = [
        [
            home_past_result,
            home_past_result,
            away_past_result,
        ]
    ]

    mock_team_stats_client.get_team_stats_for_fixture.return_value = team_stats_response

    df = match_goals.for_season(5)

    mock_result_client.GetResultsForSeason.assert_called_with(5)

    mock_team_stats_client.get_team_stats_for_fixture.assert_called_with(fixture_id=66)

    expected = [
        66,
        '4',
        3412,
        88,
        '2019-04-23T18:15:38Z',
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
        None,
        68,
        300,
        None,
        90,
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
        None,
        68,
        300,
        None,
        90,
        4
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
    value = mock_result_client.GetResultsForSeason.return_value
    value.__iter__.return_value = iter([result, result, result])

    mock_result_client.GetResultsForTeam.side_effect = [
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

    mock_result_client.GetHistoricalResultsForFixture.side_effect = [
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

    df = match_goals.for_season(5)

    mock_result_client.GetResultsForSeason.assert_called_with(5)

    assert df.shape == (3, 47)


@pytest.fixture
def mock_result_client():
    return MagicMock(spec=ResultClient)


@pytest.fixture
def mock_team_stats_client():
    return Mock(spec=TeamStatsClient)


@pytest.fixture()
def match_goals(mock_result_client, mock_team_stats_client):
    return MatchGoals(mock_result_client, mock_team_stats_client)


@pytest.fixture()
def result():
    result = result_pb2.Result()
    result.id = 66

    result.competition.id = 55
    result.competition.is_cup.value = False

    result.round.name = '4'

    result.season.id = 39910
    result.season.is_current.value = True

    result.venue.id.value = 88
    result.referee_id.value = 3412
    result.date_time = 1556043338

    result.match_data.home_team.id = 7901
    result.match_data.home_team.name = 'West Ham United'
    result.match_data.away_team.id = 496
    result.match_data.away_team.name = 'Tottenham Hotspur'
    result.match_data.stats.home_formation.value = '4-4-2'
    result.match_data.stats.away_formation.value = '5-3-1-1'
    result.match_data.stats.home_league_position.value = 3
    result.match_data.stats.away_league_position.value = 15
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
    response.home_team.passes_total.value = 300
    response.home_team.passes_percentage.value = 90
    response.home_team.possession.value = 68

    response.away_team.shots_total.value = 34
    response.away_team.shots_on_goal.value = 12
    response.away_team.shots_off_goal.value = 22
    response.away_team.shots_inside_box.value = 15
    response.away_team.shots_outside_box.value = 5
    response.away_team.passes_total.value = 300
    response.away_team.passes_percentage.value = 90
    response.away_team.possession.value = 68

    return response
