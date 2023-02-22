from typing import List

import polars as pl
from fastapi import FastAPI

from .features import InferenceFeatures
from .model import ModelInstance
from .ratings import VenueRating


def model_endpoint(recommendation_model_path: str) -> FastAPI:
    """
    Creates a FastAPI app that serves a machine learning model for making venue recommendations.

    Args:
        recommendation_model_path (str): Path to the saved machine learning model.

    Returns:
        FastAPI: A FastAPI app that serves the machine learning model.

    Raises:
        Any exceptions raised by the ModelInstance constructor.

    Example:
        >>> app = model_endpoint("path/to/recommendation/model")
        >>> uvicorn.run(app, host="0.0.0.0", port=8000)

    """
    app = FastAPI()

    model_instance = ModelInstance(
        model_artifact_bucket=recommendation_model_path,
        group_column="session_id",
        rank_column="rating",
    )

    @app.post("/predict", response_model=List[VenueRating])
    async def predict_venues_ratings(
        venues_to_be_shown: List[InferenceFeatures],
    ) -> List[VenueRating]:

        requests = [request.dict() for request in venues_to_be_shown]
        inference_dataframe = pl.DataFrame(requests)
        responses = model_instance.generate_model_ratings(inference_dataframe)
        venues_ratings = [VenueRating(**response) for response in responses]
        return venues_ratings

    return app
