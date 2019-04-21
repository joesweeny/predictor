FROM python:3.7.1

RUN apt-get update && pip install --upgrade pip

COPY ./ ./opt

RUN pip3 install pipenv
RUN cd /opt && pipenv install --system --deploy --ignore-pipfile

EXPOSE 50051
WORKDIR /opt
CMD ["python3", "-m", "predictor.grpc"]
