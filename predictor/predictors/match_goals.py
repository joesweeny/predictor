from predictor.grpc.fixture_client import FixtureClient
from predictor.data import preprocessing
from predictor.data.aggregator.match_goals import MatchGoals
from predictor.data.repository.redis import RedisRepository


class MatchGoalsPredictor:
    def __init__(self, fixture_client: FixtureClient, aggregator: MatchGoals, repository: RedisRepository):
        self.__fixture_client = fixture_client
        self.__aggregator = aggregator
        self.__repository = repository

    def predict_for_fixture(self, fixture_id: int):
        try:
            fixture = self.__fixture_client.get_fixture_by_id(fixture_id=fixture_id)
        except:
            print('Not found')
            return

        fixture_df = self.__aggregator.for_fixture(fixture=fixture)



    def __get_feature_dataframes(self, fixture):
