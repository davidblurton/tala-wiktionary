#!/bin/bash
set -e

yarn run build

docker build -t davidblurton/tala-graph-api:latest .
docker push davidblurton/tala-graph-api:latest

eval $(docker-machine env tala)
docker service update --update-failure-action rollback --image latest tala_graphql

# scp -i ~/.ssh/digitalocean stack.yml root@pianogr.am:~/tala2.yml
