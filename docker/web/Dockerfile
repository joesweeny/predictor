FROM python:3.7.2

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
    nginx \
    supervisor

COPY ./requirements.txt .
RUN pip3 install -r requirements.txt

COPY ./docker/web/uwsgi.ini /etc/uwsgi/uwsgi.ini
COPY ./docker/web/supervisord.conf /etc/supervisor/conf.d/supervisord.conf
COPY ./docker/web/nginx.conf /etc/nginx/nginx.conf
COPY . .

EXPOSE 5000
WORKDIR /opt
CMD ["/usr/bin/supervisord"]
