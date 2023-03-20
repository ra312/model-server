import os

from fastapi import FastAPI

from .endpoints.predict import router as predict
from .endpoints.search import router as search


def create_recommendation_api(recommendation_model_path: str) -> FastAPI:
    """
    Create a FastAPI instance with two endpoints for generating predicted
    venue ratings and searching for venues.

    Parameters
    ----------
    recommendation_model_path : str
        The path to the serialized machine learning model artifact.

    Returns
    -------
    FastAPI
        A FastAPI instance with two endpoints:
        - /predict: generates predicted venue ratings
        - /search: searches for venues based on location and category

    Notes
    -----
    The `recommendation_model_path` argument is used to set the
    `RECOMMENDATION_MODEL_PATH` environment variable, which is used by the
    `predict` router to load the trained machine learning model.

    The `predict` router is responsible for generating predicted venue ratings
    using the trained model. It accepts a JSON payload containing venue
    information and returns a JSON response containing predicted ratings.

    The `search` router is responsible for searching for venues based on
    location and category. It accepts query parameters for latitude, longitude,
    and category, and returns a JSON response containing venue information.
    """

    app: FastAPI = FastAPI()

    os.environ["RECOMMENDATION_MODEL_PATH"] = recommendation_model_path
    app.include_router(predict, tags=["predict"])
    app.include_router(search, tags=["search"])

    return app
