import pytest
import pandas as pd
from datetime import datetime
from mock import MagicMock, Mock, call
from predictor.framework import config
from predictor.data.repository.redis import RedisRepository
from predictor.data.aggregator.match_goals import MatchGoals
from predictor.data.handling.data_handler import DataHandler


def test_store_match_goals_data_for_supported_competitions_parses_and_stores_dataframe(handler):
    handler._configuration.SUPPORTED_COMPETITIONS = {
        0: {
            'id': 8,
            'name': 'English Premier League',
            'seasons': [
                {
                    'id': 13,
                    'name': "2016/2017",
                },
                {
                    'id': 6397,
                    'name': "2017/2018",
                },
            ]
        }
    }

    date = datetime.now()

    dataframe = pd.DataFrame.from_dict({0: {0: 'Hello'}})

    handler._aggregator.for_season.side_effect = [dataframe, dataframe, dataframe]

    handler.store_match_goals_data_for_supported_competitions(date)

    aggregrator_calls = [
        call(season_id=13, date_before=date),
        call(season_id=6397, date_before=date),
    ]

    handler._aggregator.for_season.assert_has_calls(aggregrator_calls)

    repository_calls = [
        call(key='competition:8:season:13', df=dataframe),
        call(key='competition:8:season:6397', df=dataframe),
    ]

    handler._repository.save_data_frame.assert_has_calls(repository_calls)


@pytest.fixture
def handler():
    mock_config = MagicMock(spec=config)
    mock_redis_repository = Mock(spec=RedisRepository)
    mock_aggregator = Mock(spec=MatchGoals)
    return DataHandler(mock_config, mock_redis_repository, mock_aggregator)
