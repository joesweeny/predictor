import pytest
from mock import MagicMock
from compiler.grpc.proto.event_pb2_grpc import EventServiceStub
from compiler.grpc.event_client import EventClient
from compiler.grpc.proto.event_pb2 import FixtureEventsResponse
from compiler.grpc.proto.requests_pb2 import FixtureRequest


def test_get_fixture_events_returns_a_event_fixture_response_object(grpc_stub):
    client = EventClient(client=grpc_stub)

    request = FixtureRequest(fixture_id=45)
    response = FixtureEventsResponse

    # event_stub.FixtureEvents.return_value = response
    # event_stub.FixtureEvents.assert_called_with(request=request)

    fetched = client.get_fixture_events(fixture_id=45)

    assert fetched == response


@pytest.fixture(scope='module')
def grpc_stub(grpc_channel):
    from compiler.grpc.proto.event_pb2_grpc import EventServiceStub

    return EventServiceStub(grpc_channel)
