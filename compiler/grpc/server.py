from concurrent import futures
from grpc_reflection.v1alpha import reflection
import time
import grpc
from compiler.grpc.proto.compiler import compiler_pb2_grpc, compiler_pb2
from compiler.framework.container import Container

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    compiler_pb2_grpc.add_OddsCompilerServiceServicer_to_server(
        Container().odds_compiler_service(),
        server
    )
    descriptor = compiler_pb2.DESCRIPTOR
    SERVICE_NAMES = (
        descriptor.services_by_name['OddsCompilerService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    print('Starting server. Listening on port 50052')

    server.add_insecure_port('[::]:50052')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)
