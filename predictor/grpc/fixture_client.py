import grpc
import os
from predictor.grpc.proto.fixture import fixture_pb2
from predictor.grpc.proto.fixture import fixture_pb2_grpc


class FixtureClient:
    def GetFixtureById(self, fixture_id: int) -> fixture_pb2.Fixture:
        client = self.__client()
        request = fixture_pb2.FixtureRequest(fixture_id=fixture_id)
        return client.FixtureByID(request)

    @staticmethod
    def __client():
        data_server = os.getenv('DATA_SERVER_HOST')
        channel = grpc.insecure_channel(data_server + ':50051')
        stub = fixture_pb2_grpc.FixtureServiceStub(channel)
        return stub
