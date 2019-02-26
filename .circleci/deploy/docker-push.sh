#!/bin/bash

set -e

docker login -u ${DOCKER_HUB_USERNAME} -p ${DOCKER_HUB_PASSWORD}

docker tag "statisticopredictor_grpc" "joesweeny/statisticopredictor_grpc:$CIRCLE_SHA1"
docker push "joesweeny/statisticopredictor_grpc:$CIRCLE_SHA1"
