import grpc

import proto.fixture_pb2
import proto.fixture_pb2_grpc

channel = grpc.insecure_channel('138.68.132.183:50051')

stub = proto.fixture_pb2_grpc.FixtureServiceStub(channel)

request = proto.fixture_pb2.Request(date_from='2019-02-23T00:00:00Z',date_to='2019-02-23:59:59Z')

response = stub.ListFixtures(request)

