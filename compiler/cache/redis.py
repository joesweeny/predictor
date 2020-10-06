import redis
import pandas as pd
import pyarrow as pa
from typing import Optional

EXPIRATION_SECONDS = 86400


class RedisRepository:
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client

    def save_data_frame(self, key: str, df: pd.DataFrame):
        """
        Save a Pandas dataframe to Redis store
        """
        context = pa.default_serialization_context()
        self.redis_client.setex(
            key,
            EXPIRATION_SECONDS,
            context.serialize(df).to_buffer().to_pybytes()
        )

    def get_data_frame(self, key: str) -> Optional:
        """
        Retrieve a Pandas dataframe from Redis store
        """
        value = self.redis_client.get(key)

        if value is None:
            return

        context = pa.default_serialization_context()
        return context.deserialize(value)
