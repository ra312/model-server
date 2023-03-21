import json
import os
from typing import Any

import requests
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

current_directory = os.path.dirname(__file__)


def get_local_client() -> Elasticsearch:
    return Elasticsearch("http://localhost:9200")


def create_templates() -> None:
    es = get_local_client()
    templates = ["all_results", "naive", "all_text_fields"]
    for template in templates:
        absolute_path = os.path.join(current_directory, f"./elastic/{template}.json")
        with open(absolute_path) as file:
            template_json = json.load(file)
            es.put_script(id=template, body=template_json)


def create_index() -> None:
    es = get_local_client()
    relative_filepath = "./elastic/restaurants.json"
    absolute_filepath = os.path.join(current_directory, relative_filepath)

    with open(absolute_filepath) as file:
        settings = json.load(file)
        es.indices.create(index="restaurants", body=settings)


def delete_index() -> None:
    es = get_local_client()
    if es.indices.exists(index="restaurants"):
        es.indices.delete(index="restaurants")


def index_restaurants() -> None:
    es = get_local_client()
    documents = []
    locations = [{"lat": 52.5024674, "lon": 13.2810506}]
    # locations = ["gesundbrunnen", "ostkreuz", "südkreuz", "westkreuz"]
    for location in locations:
        lat, lon = location["lat"], location["lon"]
        consumer_wolt_api_url = "https://restaurant-api.wolt.com/v1/pages/restaurants"

        params = {"lat": lat, "lon": lon}

        headers = {"app-language": "en"}

        response = requests.get(consumer_wolt_api_url, params=params, headers=headers)

        if response.status_code != 200:
            raise Exception(f"Response status code is {response.status_code}")

        restaurants: Any = response.json()

        sections = restaurants["sections"]
        items = []
        for section in sections:
            if section["name"] == "restaurants-delivering-venues":
                items = section["items"]
        for venue in items:
            document = {
                "_index": "restaurants",
                "_id": venue["venue"]["id"],
                "_source": venue,
            }
            document["_source"]["suggest"] = [venue["title"]]
            for tag in venue["venue"]["tags"]:
                document["_source"]["suggest"].append(tag)
            documents.append(document)
        bulk(es, documents)


if __name__ == "__main__":
    delete_index()
    create_index()
    index_restaurants()
    create_templates()
