from compiler.data.aggregator.match_goals import MatchGoals
from compiler.data.repository.redis import RedisRepository
from compiler.framework import config


class MatchGoalsPreProcessor:
    __key = "match-goals:competition:{}"

    def __init__(self, aggregator: MatchGoals, cache: RedisRepository, configuration: config):
        self.__aggregator = aggregator
        self.__cache = cache
        self.__configuration = configuration
