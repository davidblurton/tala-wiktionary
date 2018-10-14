#!/bin/bash
set -e

docker build -t davidblurton/tala-graph-api:latest .
docker push davidblurton/tala-graph-api:latest

# scp -i ~/.ssh/digitalocean stack.yml root@pianogr.am:~/tala2.yml
ssh root@pianogr.am -i ~/.ssh/digitalocean 'docker stack deploy -c tala2.yml tala2'
