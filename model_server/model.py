"""
Module containing a ModelInstance class, which represents a model instance and provides functionality to generate
model ratings for a given input data.
"""
import logging
from typing import Any, Dict, List

import joblib
import polars as pl


class ModelInstance:
    def __init__(self, model_artifact_bucket: str) -> None:
        """
        Initialize a new instance of the `ModelInstance` class.

        Args:
            model_artifact_bucket(str): The path to the model artifact.

        Todo:
            * Add functionality to read the model artifact from Google Cloud Storage(GCS)

        Explanation:
            For demonstration purposes, the model artifact is read locally.

        Parameters:
            model_artifact_bucket(str): The path to the trained model artifact.

            group_column(str): The name of the column
            that identifies the session ID in the input data. This parameter is
            hardcoded for each model due to the training data and re - ranking.

            rank_column(str): The name of the column
            that contains the rating values in the input data. This parameter is
            hardcoded for each model due to the training data and re - ranking.
        """
        self.model: Any = joblib.load(model_artifact_bucket)
        self.group_column = "session_id_hashed"
        self.rank_column = "popularity"

    def generate_model_ratings(self, inference_dataframe: pl.DataFrame) -> List[Dict[str, Any]]:
        """
        Generate model ratings for the given input data.

        Args:
            inference_dataframe(pl.DataFrame): A dataframe containing the input data.

        Returns:
          List[Dict[str, Any]]: A list of dictionaries,
          where each dictionary contains the venue ID and its predicted
            rating.
        """
        if "session_id_hashed" not in inference_dataframe.columns:

            inference_dataframe = inference_dataframe.with_columns(
                pl.col("session_id").str.replace("-", "").alias("session_id_hashed").hash(seed=0)
            )

        incoming_features = inference_dataframe.columns
        expected_features = self.model.feature_name()
        # EXPLAIN: does not matter here, we only construct rating
        pred_label = "predicted_label"
        predicted_rank_column = "predicted_rank"
        group_column = self.group_column
        rank_column = self.rank_column
        assert all(
            expected_column == actual_column
            for expected_column, actual_column in zip(incoming_features, expected_features)
        ), "the inference feature do not have the same order as the training features, this can lead to poorer performance"
        inference_dataframe_pd = inference_dataframe.sort(
            by=[group_column, rank_column], reverse=False
        ).to_pandas()
        inference_dataframe_pd[pred_label] = self.model.predict(inference_dataframe_pd)
        inference_dataframe_pd[predicted_rank_column] = inference_dataframe_pd.groupby(
            group_column
        )[pred_label].rank(method="first", ascending=False)
        predictions_pl = pl.DataFrame(inference_dataframe_pd)
        # Group by venue_id and compute the 80th percentile of predicted rank
        grouped = predictions_pl.groupby("venue_id").agg(
            [pl.col(predicted_rank_column).quantile(0.8).alias(f"q80_{predicted_rank_column}")]
        )

        # Select the venue_id and computed 80th percentile predicted popularity
        selected = grouped.select("venue_id", f"q80_{predicted_rank_column}")

        # Sort by venue_id
        sorted_df = selected.sort("venue_id")

        # Convert to a list of dictionaries
        ratings: List[Dict[str, Any]] = sorted_df.to_pandas().to_dict(orient="records")
        logging.info(" Returning ratings: %s", ratings)
        return ratings
