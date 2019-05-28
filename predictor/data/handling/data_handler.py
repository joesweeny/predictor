from predictor.data.repository.redis import RedisRepository
from predictor.framework import config


class MatchGoals:
    def __init__(self, config: config, repository: RedisRepository):
        self.config = config
        self.repoistory = repository

