#!/bin/bash

set -e

RELEASE=$CIRCLE_SHA1

scp docker-compose.prod.yml root@${PRODUCTION_SERVER}:~

ssh -t root@${PRODUCTION_SERVER} 'export RELEASE='"'$RELEASE'"' \

docker-compose -f ./docker-compose.prod.yml pull grpc && \

docker-compose -f ./docker-compose.prod.yml up -d'

