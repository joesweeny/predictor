import grpc
import os
import fixture_pb2
import fixture_pb2_grpc


class FixtureClient:
    def GetFixtureById(self, fixture_id):
        client = self.client()
        request = fixture_pb2.FixtureRequest(fixture_id=fixture_id)
        return client.FixtureByID(request)

    def client(self):
        data_server = os.getenv('DATA_SERVER_HOST')
        channel = grpc.insecure_channel(data_server + ':50051')
        stub = fixture_pb2_grpc.FixtureServiceStub(channel)
        return stub
