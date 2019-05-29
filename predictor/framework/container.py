import redis
from predictor.framework import config
from predictor.data.repository.redis import RedisRepository
from predictor.grpc.result_client import ResultClient
from predictor.grpc.team_stats_client import TeamStatsClient
from predictor.data.aggregator.match_goals import MatchGoals
from predictor.data.handling.data_handler import DataHandler


class Container:
    redis_client = redis.Redis(
        host=config.CONNECTIONS['redis']['host'],
        port=config.CONNECTIONS['redis']['port'],
        db=config.CONNECTIONS['redis']['database']
    )

    redis_repository = RedisRepository(redis_client=redis_client)

    result_client = ResultClient(
                        host=config.CONNECTIONS['data-server']['host'],
                        port=config.CONNECTIONS['data-server']['port'],
                    )

    team_stats_client = TeamStatsClient(
                            host=config.CONNECTIONS['data-server']['host'],
                            port=config.CONNECTIONS['data-server']['port'],
                        )

    def match_goals_aggregator(self):
        match_goals = MatchGoals(
            result_client=self.result_client,
            team_stats_client=self.team_stats_client
        )

        return match_goals

    def data_handler(self):
        data_handler = DataHandler(
            configuration=config,
            repository=self.redis_repository,
            aggregator=self.match_goals_aggregator()
        )

        return data_handler
