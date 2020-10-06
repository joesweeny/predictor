import grpc
from compiler.grpc.proto import requests_pb2
from compiler.grpc.proto import team_stats_pb2_grpc


class TeamStatsClient:
    def __init__(self, host: str, port: str):
        self.host = host
        self.port = port

    def get_team_stats_for_fixture(self, fixture_id: int):
        client = self.__client()
        request = requests_pb2.FixtureRequest(fixture_id=fixture_id)
        return client.GetTeamStatsForFixture(request)

    def __client(self):
        channel = grpc.insecure_channel(self.host + ':' + self.port)
        stub = team_stats_pb2_grpc.TeamStatsServiceStub(channel)
        return stub
