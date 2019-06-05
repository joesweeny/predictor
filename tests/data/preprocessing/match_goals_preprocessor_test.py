import pytest
from typing import Optional
from freezegun import freeze_time
from datetime import datetime
from mock import Mock, call
import pandas as pd
from predictor.data.preprocessing.match_goals import MatchGoalsPreProcessor
from predictor.data.aggregator.match_goals import MatchGoals
from predictor.data.repository.redis import RedisRepository
from predictor.framework import config


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

    preprocessor.pre_process_feature_data_for_competition(competition_id=8)

    df1 = get_season_data_frame(date='2019-05-31', stat=1.5)
    df2 = get_season_data_frame(date='2019-05-24', stat=2.5)
    df3 = get_season_data_frame(date='2019-06-05', stat=3.75)

    aggregator.for_season.side_effect = [df1, df2, df3]

    combined = pd.concat(df2, df1, df3)

    aggregator_calls = [
        call(season=13, date_before=datetime(2019, 6, 5)),
        call(season=6397, date_before=datetime(2019, 6, 5)),
    ]

    aggregator.assert_has_calls(aggregator_calls)

    cache_calls = [
        call(key='match-goals:competition:8', df=combined)
    ]

    cache.assert_has_calls(cache_calls)


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
