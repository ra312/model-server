from typing import List

import polars as pl
from fastapi import FastAPI

from .features import InferenceFeatures
from .model import ModelInstance
from .ratings import VenueRating


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

    model_instance = ModelInstance(
        model_artifact_bucket=recommendation_model_path,
        group_column="session_id",
        rank_column="rating",
    )

    @app.post("/predict", response_model=List[VenueRating])
    async def predict_venues_ratings(
        venues_to_be_shown: List[InferenceFeatures],
    ) -> List[VenueRating]:
        """
        Generate predicted venue ratings
        for a list of venues given their features.

        Args:
            venues_to_be_shown (List[InferenceFeatures]):
            A list of venue features to generate predicted ratings for.

        Returns:
            List[VenueRating]:
            A list of predicted ratings for each venue, sorted by venue ID.

        """

        requests = [request.dict() for request in venues_to_be_shown]
        inference_dataframe = pl.DataFrame(requests)
        responses = model_instance.generate_model_ratings(inference_dataframe)
        venues_ratings = [VenueRating(**response) for response in responses]
        return venues_ratings

    return app
