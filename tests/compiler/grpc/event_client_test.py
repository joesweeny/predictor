import pytest
from compiler.grpc.proto import event_pb2, event_pb2_grpc
from compiler.grpc.event_client import EventClient


def test_get_fixture_events_returns_a_fixture_event_response(grpc_stub, card_event, goal_event):
    client = EventClient(grpc_stub)

    response = client.get_fixture_events(fixture_id=45)

    assert response.fixture_id == 45
    assert len(response.cards) == 1
    assert response.cards[0] == card_event
    assert len(response.goals) == 1
    assert response.goals[0] == goal_event


@pytest.fixture(scope='module')
def grpc_add_to_server():
    from compiler.grpc.proto.event_pb2_grpc import add_EventServiceServicer_to_server

    return add_EventServiceServicer_to_server


@pytest.fixture(scope='module')
def grpc_servicer():
    return MockService


@pytest.fixture(scope='module')
def grpc_stub_cls(grpc_channel):
    from compiler.grpc.proto.event_pb2_grpc import EventServiceStub

    return EventServiceStub


@pytest.fixture()
def card_event():
    return event_pb2.CardEvent(
        id=1,
        team_id=33,
        type="redcard",
        player_id=60,
        minute=54
    )


@pytest.fixture()
def goal_event():
    return event_pb2.GoalEvent(
        id=5,
        team_id=33,
        player_id=60,
        minute=54,
        score="5-0"
    )


class MockService(event_pb2_grpc.EventServiceServicer):
    def FixtureEvents(self, request):
        response = event_pb2.FixtureEventsResponse(
            fixture_id=45,
            cards=[
                event_pb2.CardEvent(
                    id=1,
                    team_id=33,
                    type="redcard",
                    player_id=60,
                    minute=54
                )
            ],
            goals=[
                event_pb2.GoalEvent(
                    id=5,
                    team_id=33,
                    player_id=60,
                    minute=54,
                    score="5-0"
                )
            ]
        )

        return response
