import pytest
import redis
import pandas as pd
from compiler.framework import config
from compiler.data.repository.redis import RedisRepository


def test_save_data_frame_saves_to_redis_repository(redis_repository):
    values = {
        'homeTeam': 'West Ham United',
        'goalsScored': 5,
        'averageGoalsScored': 2.55
    }

    df = pd.DataFrame(values, index=[0])

    redis_repository.save_data_frame('data-1', df)

    fetched = redis_repository.get_data_frame('data-1')

    assert df.iloc[0, :].values.tolist() == fetched.iloc[0, :].values.tolist()


def test_get_data_frame_returns_none_if_key_does_not_exist(redis_repository):
    fetched = redis_repository.get_data_frame('I do not exist')

    assert fetched is None


@pytest.fixture
def redis_client():
    client = redis.Redis(
        host=config.CONNECTIONS['redis']['host'],
        port=config.CONNECTIONS['redis']['port'],
        db=config.CONNECTIONS['redis']['database']
    )

    return client


@pytest.fixture
def redis_repository(redis_client):
    return RedisRepository(redis_client=redis_client)
