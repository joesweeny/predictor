from concurrent import futures
from grpc_reflection.v1alpha import reflection
import time
import grpc
from app.grpc.proto.prediction import prediction_pb2_grpc, prediction_pb2

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class PredictionServiceServicer(prediction_pb2_grpc.PredictionServiceServicer):
    def GetForFixture(self, request, context):
        pred = prediction_pb2.Prediction(
            id=1,
            type="Over 2.5 goals",
            probability=0.75
        )
        return pred


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    prediction_pb2_grpc.add_PredictionServiceServicer_to_server(
        PredictionServiceServicer(), server
    )
    descriptor = prediction_pb2.DESCRIPTOR
    SERVICE_NAMES = (
        descriptor.services_by_name['PredictionService'].full_name,
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
