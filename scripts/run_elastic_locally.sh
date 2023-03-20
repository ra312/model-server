#!/bin/bash -e

function cleanup {
    echo "Removing Elasticsearch and Kibana containers"
    docker stop elasticsearch kibana
    docker rm elasticsearch kibana
}

echo "Stopping any running Elasticsearch and Kibana containers"
docker stop elasticsearch kibana || true
docker rm elasticsearch kibana || true

echo "pulling elasticsearch:7.13.3 image";
docker pull docker.elastic.co/elasticsearch/elasticsearch:7.13.3;

echo "pulling kibana:7.13.3 image";
docker pull docker.elastic.co/kibana/kibana:7.13.3;

echo "creating docker network for elastic and kibana"
# create if not exists
# https://stackoverflow.com/a/48643576/5444759
docker network create --driver bridge elastic || true;

echo "starting Elasticsearch"
docker run \
    --name elasticsearch \
    --net elastic \
    -p 9200:9200 \
    -e discovery.type=single-node \
    -e ES_JAVA_OPTS="-Xms1g -Xmx1g" \
    -e xpack.security.enabled=false \
    -d docker.elastic.co/elasticsearch/elasticsearch:7.13.3;

echo "starting Kibana"
docker run \
    --name kibana \
    --net elastic \
    -p 5601:5601 \
    -e ELASTICSEARCH_HOSTS=http://elasticsearch:9200 \
    -d docker.elastic.co/kibana/kibana:7.13.3;

trap cleanup EXIT;

echo "Waiting for Elasticsearch and Kibana to start up..."
sleep 30

echo "Creating index in Elasticsearch"
curl -X PUT "localhost:9200/my_index" -H 'Content-Type: application/json' -d '
{
    "settings": {
        "number_of_shards": 1,
        "number_of_replicas": 0
    }
}'

echo "Indexing sample data"
curl -X POST "localhost:9200/my_index/_doc" -H 'Content-Type: application/json' -d '
{
  "message": "Hello World"
}'

echo "Accessing Kibana UI"
echo "Please navigate to http://localhost:5601 in your web browser"
