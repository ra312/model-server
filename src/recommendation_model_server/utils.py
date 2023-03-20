import argparse
import os
import re
from typing import List


def parse_response(data: dict) -> List[dict]:
    return [
        {"image_url": item["image"]["url"], "venue_id": parse_track_id(item["image"]["url"])}
        for item in data["sections"][0]["items"]
    ]


def declare_env_variables(parsed_args: argparse.Namespace) -> None:
    os.environ["RECOMMENDATION_MODEL_PATH"] = parsed_args.recommendation_model_path


def get_recommendation_model_path() -> str:
    recommendation_model_path = os.environ.get("RECOMMENDATION_MODEL_PATH")
    if recommendation_model_path is None:
        raise ValueError("RECOMMENDATION_MODEL_PATH environment variable not set")
    return recommendation_model_path


def parse_track_id(track_id_str: str) -> str:

    # Define a regular expression pattern to match UUIDs
    uuid_pattern = re.compile(
        r"[0-9a-f]{8}-[0-9a-f]{4}-[1-5][0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}"
    )

    # Find the first UUID in the input string using the pattern
    uuid_match = uuid_pattern.search(track_id_str)

    # Extract the matched UUID string
    if not uuid_match:
        raise Exception("No UUID part found")
    return uuid_match.group(0)
