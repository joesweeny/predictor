from concurrent import futures
from dotenv import load_dotenv
from pathlib import Path
from grpc_reflection.v1alpha import reflection
import time
import grpc
import prediction_pb2_grpc
import prediction_pb2
import fixture_client

_ONE_DAY_IN_SECONDS = 60 * 60 * 24


class PredictionServiceServicer(prediction_pb2_grpc.PredictionServiceServicer):
    def GetForFixture(self, request, context):
        client = fixture_client.FixtureClient()
        response = client.GetFixture(fixture_id=request.id)
        pred = prediction_pb2.Prediction(id=request.id, type=response.home_team.name, probability=0.75)
        return pred


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    prediction_pb2_grpc.add_PredictionServiceServicer_to_server(
        PredictionServiceServicer(), server
    )
    SERVICE_NAMES = (
        prediction_pb2.DESCRIPTOR.services_by_name['PredictionService'].full_name,
        reflection.SERVICE_NAME,
    )
    reflection.enable_server_reflection(SERVICE_NAMES, server)
    print('Starting server. Listing on port 50051')
    server.add_insecure_port('grpc:50051')
    server.start()
    try:
        while True:
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


env_path = Path('.') / '/opt/app/.env'
load_dotenv(dotenv_path=env_path)

serve()
