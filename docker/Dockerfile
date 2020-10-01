FROM python:3.8.2

RUN apt-get -y update && apt-get install -y cron && pip install --upgrade pip

COPY . ./opt

RUN pip3 install pipenv
RUN cd /opt && pipenv install --dev --system --deploy --ignore-pipfile

COPY /docker/crontab /etc/cron.d/cjob

RUN chmod 0644 /etc/cron.d/cjob

WORKDIR /opt
