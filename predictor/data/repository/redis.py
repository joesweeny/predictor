import redis
import pandas as pd
from typing import Optional, List

EXPIRATION_SECONDS = 86400


class RedisRepository:
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client

    def save_data_frame(self, key: str, df: pd.DataFrame):
        """
        Save a Pandas dataframe to Redis store
        """
        self.redis_client.setex(key, EXPIRATION_SECONDS, df.to_msgpack(compress='zlib'))

    def get_data_frame(self, key: str) -> Optional:
        """
        Retrieve a Pandas dataframe from Redis store
        """
        value = self.redis_client.get(key)

        if value is None:
            return

        return pd.read_msgpack(value)

    def get_data_frames_for_competition(self, competition_id: int) -> List[pd.DataFrame]:
        """
        Retrieve multiple Pandas dataframes for a specific competition
        """
        pattern = '*competition:' + str(competition_id) + '*'

        keys = self.redis_client.keys(pattern=pattern)

        dfs = []

        for key in keys:
            dfs.append(self.get_data_frame(key))

        return dfs
