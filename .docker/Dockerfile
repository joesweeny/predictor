FROM python:3.8.5

RUN apt-get -y update && apt-get install -y cron && pip3 install --upgrade pip

RUN pip3 install pipenv
COPY Pipfile .
COPY Pipfile.lock .
RUN pipenv install --dev --system --deploy

COPY . ./opt
COPY /.docker /etc/cron.d/cronpy

RUN chmod 0644 /etc/cron.d/cronpy

WORKDIR /opt
