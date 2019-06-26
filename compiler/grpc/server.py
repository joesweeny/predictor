from concurrent import futures
from grpc_reflection.v1alpha import reflection
import time
import grpc
from compiler.grpc.proto.compiler import compiler_pb2_grpc, compiler_pb2

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class PredictionServiceServicer(compiler_pb2_grpc.CompilerServiceServicer):
    def GetOverUnderGoalsForFixture(self, request, context):
        pred = compiler_pb2.OverUnderGoalsResponse(
            id=1,
            type="Over 2.5 goals",
            probability=0.75
        )
        return pred


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    compiler_pb2_grpc.add_CompilerServiceServicer_to_server(
        PredictionServiceServicer(), server
    )
    descriptor = compiler_pb2.DESCRIPTOR
    SERVICE_NAMES = (
        descriptor.services_by_name['CompilerService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    print('Starting server. Listening on port 50051')
    server.add_insecure_port('grpc:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
