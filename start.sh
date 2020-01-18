#!/bin/bash
#
# start server with NGINX
export PATH=/usr/local/bin:$PATH
docker-compose -f docker-compose.prod.yml up -d --build
docker-compose ps
