#!/usr/bin/env bash
git pull
docker rm -f flask-composer
docker build -t bernardomrf/compositor .
docker run --name flask-composer --restart always -d -p 80:80 bernardomrf/compositor