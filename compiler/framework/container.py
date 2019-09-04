import redis
from compiler.framework import config
from compiler.data.repository.redis import RedisRepository
from compiler.grpc.fixture_client import FixtureClient
from compiler.grpc.result_client import ResultClient
from compiler.grpc.team_stats_client import TeamStatsClient
from compiler.data.aggregator.match_goals import MatchGoals
from compiler.data.preprocessing.match_goals import MatchGoalsPreProcessor
from compiler.data.handling.data_handler import DataHandler


class Container:
    __configuration = config

    redis_client = redis.Redis(
        host=config.CONNECTIONS['redis']['host'],
        port=config.CONNECTIONS['redis']['port'],
        db=config.CONNECTIONS['redis']['database']
    )

    redis_repository = RedisRepository(redis_client=redis_client)

    fixture_client = FixtureClient(
                        host=config.CONNECTIONS['data-server']['host'],
                        port=config.CONNECTIONS['data-server']['port'],
                    )

    result_client = ResultClient(
                        host=config.CONNECTIONS['data-server']['host'],
                        port=config.CONNECTIONS['data-server']['port'],
                    )

    team_stats_client = TeamStatsClient(
                            host=config.CONNECTIONS['data-server']['host'],
                            port=config.CONNECTIONS['data-server']['port'],
                        )

    def get_config(self):
        return self.__configuration

    def match_goals_aggregator(self):
        return MatchGoals(result_client=self.result_client, team_stats_client=self.team_stats_client)

    def match_goals_pre_processor(self):
        processor = MatchGoalsPreProcessor(
            aggregator=self.match_goals_aggregator(),
            cache=self.redis_repository,
            configuration=config
        )

        return processor

    def data_handler(self):
        handler = DataHandler(
            configuration=config,
            repository=self.redis_repository,
            aggregator=self.match_goals_aggregator()
        )

        return handler
