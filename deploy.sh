#!/bin/bash
set -euo pipefail

: ${CIRCLE_SHA1:=$(git rev-parse --verify HEAD)}
REGISTRY=davidblurton
PROJECT=tala-graph-api
TAG=$REGISTRY/$PROJECT:$CIRCLE_SHA1
TAG_LATEST=$REGISTRY/$PROJECT:latest

yarn run build

docker build -t $TAG_LATEST -t $TAG .
docker push $TAG
docker push $TAG_LATEST

eval $(docker-machine env tala)
docker service update --update-failure-action rollback --image $TAG tala_graphql
docker service ps tala_graphql
