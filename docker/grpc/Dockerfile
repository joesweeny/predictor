FROM python:3.7.2

RUN apt-get update

COPY ./ ./opt

RUN pip3 install pipenv
RUN cd /opt && pipenv install --system --deploy --ignore-pipfile

EXPOSE 50051
WORKDIR /opt
CMD ["python3", "-m", "app"]
