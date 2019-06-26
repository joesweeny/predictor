import grpc
from compiler.grpc.proto.fixture import fixture_pb2
from compiler.grpc.proto.fixture import fixture_pb2_grpc


class FixtureClient:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def get_fixture_by_id(self, fixture_id: int) -> fixture_pb2.Fixture:
        client = self.__client()
        request = fixture_pb2.FixtureRequest(fixture_id=fixture_id)
        return client.FixtureByID(request)

    def __client(self):
        channel = grpc.insecure_channel(self.host + ':' + self.port)
        stub = fixture_pb2_grpc.FixtureServiceStub(channel)
        return stub
