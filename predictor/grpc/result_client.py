import grpc
from predictor.grpc.proto.result import result_pb2
from predictor.grpc.proto.result import result_pb2_grpc
from google.protobuf import wrappers_pb2


class ResultClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def GetResultsForSeason(self, season_id: int):
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
            home_team_id: int,
            away_team_id: int,
            date_before: str,
            limit: int = None
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

    def __client(self):
        channel = grpc.insecure_channel(self.host + ':' + self.port)
        stub = result_pb2_grpc.ResultServiceStub(channel)
        return stub
