# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from compiler.grpc.proto.stats.team import stats_pb2 as compiler_dot_grpc_dot_proto_dot_stats_dot_team_dot_stats__pb2


class TeamStatsServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetTeamStatsForFixture = channel.unary_unary(
        '/team_stats.TeamStatsService/GetTeamStatsForFixture',
        request_serializer=compiler_dot_grpc_dot_proto_dot_stats_dot_team_dot_stats__pb2.FixtureRequest.SerializeToString,
        response_deserializer=compiler_dot_grpc_dot_proto_dot_stats_dot_team_dot_stats__pb2.StatsResponse.FromString,
        )


class TeamStatsServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def GetTeamStatsForFixture(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_TeamStatsServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetTeamStatsForFixture': grpc.unary_unary_rpc_method_handler(
          servicer.GetTeamStatsForFixture,
          request_deserializer=compiler_dot_grpc_dot_proto_dot_stats_dot_team_dot_stats__pb2.FixtureRequest.FromString,
          response_serializer=compiler_dot_grpc_dot_proto_dot_stats_dot_team_dot_stats__pb2.StatsResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'team_stats.TeamStatsService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))