#!/bin/bash

set -e

RELEASE=$CIRCLE_SHA1
DATA_SERVER_HOST=${DATA_SERVER_HOST}
DATA_SERVER_PORT=${DATA_SERVER_PORT}

scp docker-compose.prod.yml root@${PRODUCTION_SERVER}:~

ssh -t root@${PRODUCTION_SERVER} 'export RELEASE='"'$RELEASE'"' export DATA_SERVER_HOST='"'$DATA_SERVER_HOST'"' export DATA_SERVER_PORT='"'$DATA_SERVER_PORT'"' \

docker-compose -f ./docker-compose.prod.yml pull grpc && \

docker-compose -f ./docker-compose.prod.yml up -d'

