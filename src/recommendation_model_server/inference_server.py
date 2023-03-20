import os

from fastapi import FastAPI

from .endpoints.predict import router as predict
from .endpoints.search import router as search


def model_endpoint(recommendation_model_path: str) -> FastAPI:
    """
    This function creates a FastAPI instance
    with a single endpoint for generating
    predicted venue ratings
    using a trained machine learning model.
    Args:
        recommendation_model_path (str):
        The path to the serialized
        machine learning model artifact.
    Returns:
        FastAPI: A FastAPI instance with a single endpoint
        for generating predicted venue ratings.
    """

    app = FastAPI()

    os.environ["RECOMMENDATION_MODEL_PATH"] = recommendation_model_path
    app.include_router(predict, tags=["predict"])
    app.include_router(search, tags=["search"])

    return app
