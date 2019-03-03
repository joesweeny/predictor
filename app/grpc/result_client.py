import grpc
import os
import result_pb2
import result_pb2_grpc


class ResultClient:
    def GetResultsForTeam(self, team_id, limit, date_before):
        client = self.client()
        request = result_pb2.TeamRequest(team_id=team_id, limit=limit, date_before=date_before)
        return client.GetResultsForTeam(request)

    def client(self):
        data_server = os.getenv('DATA_SERVER_HOST')
        channel = grpc.insecure_channel(data_server + ':50051')
        stub = result_pb2_grpc.ResultServiceStub(channel)
        return stub
