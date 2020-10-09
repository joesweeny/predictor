from concurrent import futures
import grpc
from grpc_reflection.v1alpha import reflection
from compiler.grpc.proto import compiler_pb2_grpc, compiler_pb2
from compiler.framework.container import Container

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


def serve():
    container = Container()

    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    compiler_pb2_grpc.add_OddsCompilerServiceServicer_to_server(
        container.odds_compiler_service(),
        server
    )
    print('Starting server. Listening on port 50052')

    SERVICE_NAMES = (
        compiler_pb2.DESCRIPTOR.services_by_name['OddsCompilerService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)

    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()
