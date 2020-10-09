from compiler.models.odds import Odds
from compiler.grpc.proto import compiler_pb2_grpc, compiler_pb2
from compiler.models.over_under_goals import OverUnderGoalsModel
from typing import List


class OddsCompilerServiceServicer(compiler_pb2_grpc.OddsCompilerServiceServicer):
    def __init__(self, over_under_model: OverUnderGoalsModel):
        self.__over_under_model = over_under_model

    def GetEventMarket(self, request, context):
        odds = []

        if request.market == 'OVER_UNDER_25':
            odds = self.__over_under_model.get_odds(fixture_id=request.event_id)

        response = compiler_pb2.EventMarket(
            event_id=request.event_id,
            market=request.market,
            odds=self.__map_odds(odds)
        )

        return response

    @staticmethod
    def __map_odds(odds: List[Odds]) -> List[compiler_pb2.Odds]:
        mapped = []

        for o in odds:
            odd = compiler_pb2.Odds(price=o.get_price(), selection=o.get_selection())
            mapped.append(odd)

        return mapped
