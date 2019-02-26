FROM python:3.7.2

RUN apt-get update

COPY . .

RUN pip3 install pipenv
RUN pipenv install --system --deploy --ignore-pipfile

EXPOSE 50051
WORKDIR /opt
CMD ["python3", "/opt/app/grpc/server.py"]
