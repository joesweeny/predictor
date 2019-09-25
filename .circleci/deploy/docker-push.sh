#!/bin/bash

set -e

docker login -u ${DOCKER_HUB_USERNAME} -p ${DOCKER_HUB_PASSWORD}

docker tag "statisticooddscompiler_grpc" "joesweeny/statisticooddscompiler_grpc:$CIRCLE_SHA1"
docker push "joesweeny/statisticooddscompiler_grpc:$CIRCLE_SHA1"

docker tag "statisticooddscompiler_console" "joesweeny/statisticooddscompiler_console:$CIRCLE_SHA1"
docker push "joesweeny/statisticooddscompiler_console:$CIRCLE_SHA1"

docker tag "statisticooddscompiler_cron" "joesweeny/statisticooddscompiler_cron:$CIRCLE_SHA1"
docker push "joesweeny/statisticooddscompiler_cron:$CIRCLE_SHA1"
