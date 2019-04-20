import grpc
import os
from app.grpc.proto.result import result_pb2
from app.grpc.proto.result import result_pb2_grpc
from google.protobuf import wrappers_pb2


class ResultClient:
    def GetResultsForSeason(self, season_id):
        client = self.__client()
        request = result_pb2.SeasonRequest(season_id=season_id)
        for result in client.GetResultsForSeason(request):
            yield result

    def GetResultsForTeam(self, team_id, limit, date_before):
        client = self.__client()
        limit = wrappers_pb2.Int32Value(value=limit)
        request = result_pb2.TeamRequest(
            team_id=team_id,
            limit=limit,
            date_before=date_before
        )
        for result in client.GetResultsForTeam(request):
            yield result

    def GetHistoricalResultsForFixture(
            self,
            home_team_id,
            away_team_id,
            limit,
            date_before
    ):
        client = self.__client()
        request = result_pb2.HistoricalResultRequest(
            home_team_id=home_team_id,
            away_team_id=away_team_id,
            limit=limit,
            date_before=date_before
        )
        for result in client.GetHistoricalResultsForFixture(request):
            yield result

    @staticmethod
    def __client():
        data_server = os.getenv('DATA_SERVER_HOST')
        channel = grpc.insecure_channel(data_server + ':50051')
        stub = result_pb2_grpc.ResultServiceStub(channel)
        return stub
