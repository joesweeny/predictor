import pytest
import mock
from typing import Optional
from freezegun import freeze_time
from datetime import datetime, timezone
from mock import Mock, call
import pandas as pd
from compiler.data.preprocessing.match_goals import MatchGoalsPreProcessor
from compiler.data.aggregator.match_goals import MatchGoals
from compiler.data.repository.redis import RedisRepository
from compiler.framework import config
from compiler.framework.exception import DataPreProcessingException


@freeze_time('2019-06-05')
def test_pre_process_feature_data_for_competition_aggregates_historic_data_and_saves_to_cache(
    preprocessor,
    aggregator,
    cache,
    configuration
):
    preprocessor = MatchGoalsPreProcessor(
        aggregator=aggregator,
        cache=cache,
        configuration=configuration
    )

    df1 = get_season_data_frame(date='2019-05-31', stat=1.5)
    df2 = get_season_data_frame(date='2019-05-24', stat=2.5)

    aggregator.for_season.side_effect = [df1, df2]

    preprocessor.pre_process_feature_data_for_competition(competition_id=8)

    aggregator_calls = [
        call(season_id=13, date_before=datetime(2019, 6, 5, 0, 0, tzinfo=timezone.utc)),
        call(season_id=6397, date_before=datetime(2019, 6, 5, 0, 0, tzinfo=timezone.utc))
    ]

    aggregator.for_season.assert_has_calls(aggregator_calls)

    cache_calls = [
        call(key='match-goals:competition:8', df=mock.ANY)
    ]

    cache.save_data_frame.assert_has_calls(cache_calls)


def test_pre_process_feature_data_raises_exception_if_competition_is_not_supported(
    preprocessor,
    aggregator,
    cache,
    configuration
):
    preprocessor = MatchGoalsPreProcessor(
        aggregator=aggregator,
        cache=cache,
        configuration=configuration
    )

    aggregator.for_season.side_effect = []

    with pytest.raises(DataPreProcessingException):
        preprocessor.pre_process_feature_data_for_competition(competition_id=999)


@pytest.fixture
def preprocessor(configuration):
    aggregator = Mock(spec=MatchGoals)
    cache = Mock(spec=RedisRepository)
    return MatchGoalsPreProcessor(aggregator=aggregator, cache=cache, configuration=configuration)


@pytest.fixture
def aggregator():
    return Mock(spec=MatchGoals)


@pytest.fixture
def cache():
    return Mock(spec=RedisRepository)


@pytest.fixture
def configuration():
    config.SUPPORTED_COMPETITIONS = {
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
    return config


def get_season_data_frame(date: str, stat: Optional):
    row = {
        'date': pd.Timestamp(date),
        'formation': '4-4-2',
        'shotsOnGoal': stat
    }
    return pd.DataFrame([row])
