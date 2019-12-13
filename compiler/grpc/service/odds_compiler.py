from compiler.grpc.proto.compiler import compiler_pb2_grpc, compiler_pb2
from compiler.grpc.fixture_client import FixtureClient
from compiler.data.handling.data_handler import DataHandler
from compiler.model.match_goals import xg, xg_shot_ratio


class OddsCompilerServiceServicer(compiler_pb2_grpc.OddsCompilerServiceServicer):
    def __init__(self, fixture_client: FixtureClient, handler: DataHandler):
        self.__fixture_client = fixture_client
        self.__handler = handler

    def GetOverUnderGoalsForFixture(self, request, context):
        fixture = self.__fixture_client.get_fixture_by_id(fixture_id=request.fixture_id)

        fix_data = self.__handler.get_match_goals_data_for_fixture(fixture_id=fixture.id)

        train_data = self.__handler.get_stored_match_goals_data_for_competition(
            competition_id=fixture.competition.id
        )

        model = xg.train_glm_model(features=train_data)

        odds = xg.get_over_under_odds(model=model, fixture=fix_data.to_dict('records')[0])

        one = compiler_pb2.ModelResult(
            fixture_id=fixture.id,
            model_name=odds.get_model_name(),
            under=odds.get_under_decimal_odds(),
            over=odds.get_over_decimal_odds()
        )

        model = xg_shot_ratio.train_glm_model(features=train_data)

        odds = xg_shot_ratio.get_over_under_odds(model=model, fixture=fix_data.to_dict('records')[0])

        two = compiler_pb2.ModelResult(
            fixture_id=fixture.id,
            model_name=odds.get_model_name(),
            under=odds.get_under_decimal_odds(),
            over=odds.get_over_decimal_odds()
        )

        response = compiler_pb2.OverUnderGoalsResponse(
            models=[one, two]
        )

        return response
