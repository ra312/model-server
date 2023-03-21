#!/bin/bash -e

function cleanup {
    echo "Removing Elasticsearch and Kibana containers"
    docker stop kibana
    docker rm kibana
}

echo "Clean up any existing containers"
cleanup
echo "pulling kibana:7.13.3 image";
docker pull docker.elastic.co/kibana/kibana:7.13.3;

echo "starting kibana"
docker run --name kibana --net elastic -p 5601:5601 -e ELASTICSEARCH_HOSTS=http://elasticsearch:9200 -it docker.elastic.co/kibana/kibana:7.13.3;

echo "Waiting for Elasticsearch and Kibana to start up..."
sleep 30

trap cleanup EXIT;
