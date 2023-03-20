from typing import Any, List

import requests
from fastapi import APIRouter

from ..restaurant import RestaurantDetails
from ..utils import parse_response

router = APIRouter()


@router.get("/search/", response_model=List[RestaurantDetails])
async def search_restaurants(
    lat: float = 52.5024674, lon: float = 13.2810506
) -> List[RestaurantDetails]:
    """
    Search for nearby restaurants using Wolt API.

    Args:
        lat (float): Latitude of the location to search for restaurants.
        lon (float): Longitude of the location to search for restaurants.

    Returns:
        List[RestaurantDetails]: List of nearby restaurants details.
    """

    consumer_wolt_api_url = "https://restaurant-api.wolt.com/v1/pages/restaurants"

    params = {"lat": lat, "lon": lon}

    headers = {"app-language": "en"}

    response = requests.get(consumer_wolt_api_url, params=params, headers=headers)

    if response.status_code != 200:
        raise Exception(f"Response status code is {response.status_code}")

    restaurant_data: Any = response.json()
    restaurants = parse_response(restaurant_data)
    return [RestaurantDetails(**restaurant) for restaurant in restaurants]
