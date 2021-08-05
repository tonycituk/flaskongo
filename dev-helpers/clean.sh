#!/bin/bash
docker-compose down
vlmns=$(docker volume ls -q)
docker volume rm $vlmns
tree ./mongodb
sudo rm -rf ./mongodb/db/
mkdir ./mongodb/db
tree ./mongodb