#!/bin/bash

set -e

mkdir -p /tmp/workspace/docker-cache

docker save -o /tmp/workspace/docker-cache/statisticooddscompiler_grpc.tar statisticooddscompiler_grpc:latest
