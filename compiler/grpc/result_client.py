import grpc
from compiler.grpc.proto import result_pb2_grpc
from compiler.grpc.proto import requests_pb2


class ResultClient:
    def __init__(self, host: str, port: str):
        self.host = host
        self.port = port

    def get_results_for_season(self, season_id: int, date_before: str):
        client = self.__client()
        request = requests_pb2.SeasonRequest(season_id=season_id, date_before=date_before)
        for result in client.GetResultsForSeason(request):
            yield result

    def __client(self):
        channel = grpc.insecure_channel(self.host + ':' + self.port)
        stub = result_pb2_grpc.ResultServiceStub(channel)
        return stub
