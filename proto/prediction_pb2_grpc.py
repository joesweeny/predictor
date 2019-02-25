# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from proto import prediction_pb2 as proto_dot_prediction__pb2


class PredictionServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.GetForFixture = channel.unary_unary(
        '/prediction.PredictionService/GetForFixture',
        request_serializer=proto_dot_prediction__pb2.Fixture.SerializeToString,
        response_deserializer=proto_dot_prediction__pb2.Prediction.FromString,
        )


class PredictionServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def GetForFixture(self, request, context):
    """A simple RPC.

    Returns a prediction for a given fixture
    """
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_PredictionServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'GetForFixture': grpc.unary_unary_rpc_method_handler(
          servicer.GetForFixture,
          request_deserializer=proto_dot_prediction__pb2.Fixture.FromString,
          response_serializer=proto_dot_prediction__pb2.Prediction.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'prediction.PredictionService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
