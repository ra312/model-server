from typing import List

import polars as pl
import uvicorn
from fastapi import FastAPI

from .features import InferenceFeatures
from .model import ModelInstance
from .ratings import VenueRating


def model_endpoint() -> None:

    app = FastAPI()

    model_instance = ModelInstance(
        model_artifact_bucket="/workspaces/model-server/rate_venues.pickle",
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

    host = "0.0.0.0"
    port = "8080"
    uvicorn.run(app, host=host, port=int(port))
