#!/bin/bash -e

function cleanup {
    echo "Removing Elasticsearch and Kibana containers"
    docker stop elasticsearch
    docker rm elasticsearch

}


echo "pulling elasticsearch:7.13.3 image";
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.13.3;

echo "creating docker network for elastic and kibana"


# https://stackoverflow.com/a/48643576/5444759
docker network create --driver bridge elastic || true;

echo "Stopping any running Elasticsearch containers"
docker stop elasticsearch
docker rm elasticsearch


echo "starting elastic"
docker run --name elasticsearch --net elastic -p 9200:9200 -e discovery.type=single-node -e ES_JAVA_OPTS="-Xms1g -Xmx1g" -e xpack.security.enabled=false -it docker.elastic.co/elasticsearch/elasticsearch:7.13.3;



echo "Waiting for Elasticsearch and Kibana to start up..."
sleep 30

trap cleanup EXIT;
