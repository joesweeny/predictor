import redis
import pandas as pd

EXPIRATION_SECONDS = 86400


class RedisRepository:
    def __init__(self, redis_client: redis.Redis):
        self.redis_client = redis_client

    def save_data_frame(self, key: str, df: pd.DataFrame):
        self.redis_client.setex(key, EXPIRATION_SECONDS, df.to_msgpack(compress='zlib'))

    def get_data_frame(self, key: str) -> pd.DataFrame:
        return pd.read_msgpack(self.redis_client.get(key))
