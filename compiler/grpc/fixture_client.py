import grpc
from compiler.grpc.proto import fixture_pb2
from compiler.grpc.proto import requests_pb2
from compiler.grpc.proto import fixture_pb2_grpc


class FixtureClient:
    def __init__(self, host: str, port: str):
        self.host = host
        self.port = port

    def get_fixture_by_id(self, fixture_id: int) -> fixture_pb2.Fixture:
        client = self.__client()
        request = requests_pb2.FixtureRequest(fixture_id=fixture_id)
        return client.FixtureByID(request)

    def __client(self):
        channel = grpc.insecure_channel(self.host + ':' + self.port)
        stub = fixture_pb2_grpc.FixtureServiceStub(channel)
        return stub
