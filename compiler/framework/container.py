import redis
from compiler.framework import config
from compiler.cache.redis import RedisRepository
from compiler.grpc.fixture_client import FixtureClient
from compiler.grpc.result_client import ResultClient
from compiler.grpc.team_stats_client import TeamStatsClient
from compiler.preprocessing.aggregation.goals import GoalsAggregator
from compiler.data_handling.goals import GoalsDataHandler
from compiler.models.over_under_goals import OverUnderGoalsModel
from compiler.grpc.service.odds_compiler import OddsCompilerServiceServicer
from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):
    # Configuration
    configuration = providers.Configuration()

    configuration.from_dict(config.config_factory())

    # Connections
    redis_client = providers.Singleton(
        redis.Redis,
        host=configuration.connections.redis.host,
        port=configuration.connections.redis.port,
        db=configuration.connections.redis.database,
    )

    data_service_host = configuration.connections.data_server.host
    data_service_port = configuration.connections.data_server.port

    # Gateways
    fixture_client = providers.Singleton(FixtureClient, host=data_service_host, port=data_service_port)
    result_client = providers.Singleton(ResultClient, host=data_service_host, port=data_service_port)
    team_stats_client = providers.Singleton(TeamStatsClient, host=data_service_host, port=data_service_port)

    # Repositories
    redis_repository = providers.Singleton(RedisRepository, redis_client=redis_client)

    # Services
    goals_aggregator = providers.Singleton(
        GoalsAggregator,
        fixture_client=fixture_client,
        result_client=result_client,
        team_stats_client=team_stats_client
    )

    goals_data_handler = providers.Singleton(
        GoalsDataHandler,
        competitions=configuration.supported_competitions,
        repository=redis_repository,
        aggregator=goals_aggregator,
    )

    # Models

    over_under_model = providers.Singleton(OverUnderGoalsModel, handler=goals_data_handler)

    # gRPC

    odds_compiler_service = providers.Singleton(OddsCompilerServiceServicer, over_under_model=over_under_model)
