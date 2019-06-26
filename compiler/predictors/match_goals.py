from compiler.grpc.fixture_client import FixtureClient
from compiler.data.preprocessing.match_goals import MatchGoalsPreProcessor
from compiler.model.match_goals import predict_match_goals


class MatchGoalsPredictor:
    def __init__(self, fixture_client: FixtureClient, preprocessor: MatchGoalsPreProcessor):
        self.__fixture_client = fixture_client
        self.__preprocessor = preprocessor

    def predict_for_fixture(self, fixture_id: int):
        try:
            fixture = self.__fixture_client.get_fixture_by_id(fixture_id=fixture_id)
        except Exception:
            raise Exception('Fixture {} does not exist'.format(fixture_id))

        features, predict = self.__preprocessor.pre_process_data_for_fixture(fixture=fixture)

        return predict_match_goals(features=features, fixture=predict)
