import grpc
from compiler.grpc.exception import GRPCException
from compiler.grpc.proto.event_pb2 import FixtureEventsResponse
from compiler.grpc.proto.requests_pb2 import FixtureRequest
from compiler.grpc.proto.event_pb2_grpc import EventServiceStub


class EventClient:
    def __init__(self, client: EventServiceStub):
        self.client = client

    def get_fixture_events(self, fixture_id: int) -> FixtureEventsResponse:
        request = FixtureRequest(fixture_id=fixture_id)

        try:
            response = self.client.FixtureEvents(request)
        except grpc.RpcError as e:
            raise GRPCException(code=e.code(), message=e.details())

        return response
