import pytest
import pandas as pd
from datetime import datetime
from mock import MagicMock, Mock, call
from compiler.framework import config
from compiler.data.repository.redis import RedisRepository
from compiler.data.aggregator.match_goals import MatchGoals
from compiler.data.handling.data_handler import DataHandler


def test_store_match_goals_data_for_supported_competitions_parses_and_stores_data_frame(handler):
    pass
    # handler._configuration.SUPPORTED_COMPETITIONS = {
    #     0: {
    #         'id': 8,
    #         'name': 'English Premier League',
    #         'seasons': [
    #             {
    #                 'id': 13,
    #                 'name': "2016/2017",
    #             },
    #             {
    #                 'id': 6397,
    #                 'name': "2017/2018",
    #             },
    #         ]
    #     }
    # }
    #
    # date = datetime.now()
    #
    # dataframe = pd.read_csv("/opt/tests/test-data/test-data.csv")
    #
    # df = dataframe[-180:]
    #
    # handler._aggregator.for_season.side_effect = [df, df]
    #
    # handler.store_match_goals_data_for_supported_competitions(date)
    #
    # aggregrator_calls = [
    #     call(season_id=13, date_before=date),
    #     call(season_id=6397, date_before=date),
    # ]
    #
    # handler._aggregator.for_season.assert_has_calls(aggregrator_calls)
    #
    # repository_calls = [
    #     call(key='competition:8:match_goals.csv', df=dataframe),
    # ]
    #
    # handler._repository.save_data_frame.assert_has_calls(repository_calls)


def test_get_stored_match_goals_data_for_competition_returns_stored_dataframe(handler):
    pass

@pytest.fixture
def handler():
    mock_config = MagicMock(spec=config)
    mock_redis_repository = Mock(spec=RedisRepository)
    mock_aggregator = Mock(spec=MatchGoals)
    return DataHandler(mock_config, mock_redis_repository, mock_aggregator)
