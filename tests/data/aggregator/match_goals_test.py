import pytest
from mock import MagicMock
from predictor.data.aggregator.match_goals import MatchGoals
from predictor.grpc.proto.result import result_pb2
from predictor.grpc.result_client import ResultClient


def test_for_season_dataframe_columns(mock_result_client, match_goals):
    value = mock_result_client.GetResultsForSeason.return_value
    value.__iter__.return_value = iter([])

    df = match_goals.ForSeason(5)

    mock_result_client.GetResultsForSeason.assert_called_with(5)

    columns = [
        'Match ID',
        'Home Team ID',
        'Away Team ID',
        'Competition ID',
        'Is Cup',
        'Season ID',
        'Is Current Season',
        'Referee ID',
        'Venue ID',
        'Date',
        'Home Days Since Last Match',
        'Away Days Since Last Match',
        'Home League Position',
        'Away League Position',
        'Home Formation',
        'Away Formation',
        'Home Avg Goals Scored Last 20',
        'Home Avg Goals Conceded Last 20',
        'Away Avg Goals Scored Last 20',
        'Away Avg Goals Conceded Last 20',
        'Home Goals in Lineup',
        'Away Goals in Lineup',
        'Average Goals for Fixture',
        'Total Goals in Match',
    ]

    df_columns = df.columns

    assert (df_columns == columns).all()


def test_for_season_converts_result_object_into_dataframe_row(
    mock_result_client,
    match_goals,
    result
):
    value = mock_result_client.GetResultsForSeason.return_value
    value.__iter__.return_value = iter([result])

    df = match_goals.ForSeason(5)

    mock_result_client.GetResultsForSeason.assert_called_with(5)

    expected = [
        66,
        7901,
        496,
        55,
        False,
        39910,
        True,
        3412,
        88,
        1556043338,
        'Calculate Home Days',
        'Calculate Away Days',
        3,
        15,
        '4-4-2',
        '5-3-1-1',
        'Calculate Home Goals Scored',
        'Calculate Away Goals Scored',
        'Calculate Home Goals Conceded',
        'Calculate Away Goals Conceded',
        'Calculate Home Goals in Lineup',
        'Calculate Away Goals in Lineup',
        'Calculate Average Goals for Fixture',
        4
    ]

    row = df.iloc[0, :].values.tolist()

    assert row == expected


def test_for_reason_populates_multiple_rows_of_data_for_multiple_results(
    mock_result_client,
    match_goals,
    result
):
    value = mock_result_client.GetResultsForSeason.return_value
    value.__iter__.return_value = iter([result, result, result])

    df = match_goals.ForSeason(5)

    mock_result_client.GetResultsForSeason.assert_called_with(5)

    assert df.shape == (3, 24)


@pytest.fixture
def mock_result_client():
    return MagicMock(spec=ResultClient)


@pytest.fixture()
def match_goals(mock_result_client):
    return MatchGoals(mock_result_client)


@pytest.fixture()
def result():
    result = result_pb2.Result()
    result.id = 66

    result.competition.id = 55
    result.competition.is_cup.value = False

    result.season.id = 39910
    result.season.is_current.value = True

    result.venue.id.value = 88
    result.referee_id.value = 3412
    result.date_time = 1556043338

    result.match_data.home_team.id = 7901
    result.match_data.away_team.id = 496
    result.match_data.stats.home_formation.value = '4-4-2'
    result.match_data.stats.away_formation.value = '5-3-1-1'
    result.match_data.stats.home_league_position.value = 3
    result.match_data.stats.away_league_position.value = 15
    result.match_data.stats.home_score.value = 2
    result.match_data.stats.away_score.value = 2

    return result
