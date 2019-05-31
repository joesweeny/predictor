import pytest
import redis
import pandas as pd
from predictor.framework import config
from predictor.data.repository.redis import RedisRepository


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


def test_get_data_frames_for_competition_returns_a_list_of_data_frames(redis_repository):
    redis_repository.redis_client.flushall()

    row = {
        'goals': 4
    }

    df = pd.DataFrame(row, index=[0])

    redis_repository.save_data_frame('competition:5:season:1', df)
    redis_repository.save_data_frame('competition:5:season:2', df)
    redis_repository.save_data_frame('competition:5:season:3', df)
    redis_repository.save_data_frame('competition:8:season:1', df)

    dfs = redis_repository.get_data_frames_for_competition(competition_id=5)

    assert 3 == len(dfs)

    for df in dfs:
        assert isinstance(df, pd.DataFrame)


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
