import grpc
from compiler.grpc.proto.result import result_pb2
from compiler.grpc.proto.result import result_pb2_grpc
from google.protobuf import wrappers_pb2


class ResultClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def get_results_for_season(self, season_id: int, date_before: str):
        client = self.__client()
        request = result_pb2.SeasonRequest(season_id=season_id, date_before=date_before)
        for result in client.GetResultsForSeason(request):
            yield result

    def get_results_for_team(self, team_id, limit, date_before):
        client = self.__client()
        limit = wrappers_pb2.Int32Value(value=limit)
        request = result_pb2.TeamRequest(
            team_id=team_id,
            limit=limit,
            date_before=date_before
        )

        results = []

        for result in client.GetResultsForTeam(request):
            results.append(result)

        return results

    def get_historical_results_for_fixture(
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

        results = []

        for result in client.GetHistoricalResultsForFixture(request):
            results.append(result)

        return results

    def __client(self):
        channel = grpc.insecure_channel(self.host + ':' + self.port)
        stub = result_pb2_grpc.ResultServiceStub(channel)
        return stub
