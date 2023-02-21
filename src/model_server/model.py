from typing import Any, Dict, List

import joblib
import polars as pl


class ModelInstance:
    def __init__(self, model_artifact_bucket: str, group_column: str, rank_column: str):
        # TODO: add reading from gcs
        # EXPLAIN: for demo, we read locally

        self.model: Any = joblib.load(model_artifact_bucket)
        self.group_column = f"{group_column}_hashed"
        self.rank_column = rank_column

    def generate_model_ratings(self, inference_dataframe: pl.DataFrame) -> List[Dict[str, Any]]:
        # inference_dataframe = pl.DataFrame(
        #     json.loads(incoming_inference_features_str))
        # hashed_session_column = f"{self.group_column}_hashed"
        # if 'session_id' not in inference_dataframe.columns:
        #     raise RuntimeWarning(
        #         "'session_id' column not found in incoming request")
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
        ratings: List[Dict[str, Any]] = (
            predictions_pl.groupby("venue_id")
            .agg(
                [pl.col(predicted_rank_column).quantile(0.8).alias(f"q80_{predicted_rank_column}")]
            )
            .select("venue_id", f"q80_{predicted_rank_column}")
            .sort("venue_id")
            .to_pandas()
            .to_dict(orient="records")
        )
        print(f" Returning ratings={ratings}")
        return ratings
