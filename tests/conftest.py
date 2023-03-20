import logging.config
from typing import Any

import pytest
from fastapi import FastAPI

from recommendation_model_server.recommendation_api import create_recommendation_api


@pytest.fixture(scope="session", autouse=True)
def setup_logging() -> Any:
    return logging.config.dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "handlers": {
                "console": {
                    "class": "logging.StreamHandler",
                    "level": "INFO",
                    "formatter": "basic",
                },
            },
            "formatters": {
                "basic": {
                    "format": "%(asctime)s [%(levelname)s] %(message)s",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                },
            },
            "root": {
                "handlers": ["console"],
                "level": "DEBUG",
            },
        }
    )


@pytest.fixture(scope="module")
def app() -> FastAPI:
    return create_recommendation_api("artifacts/rate_venues.pickle")


@pytest.fixture(scope="module")
def request_body() -> dict:
    return {
        "venue_id": -4202398962129790000,
        "conversions_per_impression": 0.3556765815,
        "price_range": 1,
        "rating": 8.6,
        "popularity": 4.4884057024,
        "retention_rate": 8.6,
        "session_id_hashed": 3352618370338455600,
        "position_in_list": 31,
        "is_from_order_again": 0,
        "is_recommended": 0,
    }
