import joblib
import lightgbm as lgb
import json
import polars as pl


class ModelInstance:
    def __init__(self, model_artifact_bucket: str,
    group_column: str, rank_column: str):
        # TODO: add reading from gcs
        # EXPLAIN: for demo, we read locally


        # Load the model from the pickled file
        self.model: lgb.Booster = joblib.load(model_artifact_bucket)
        self.group_column = group_column
        self.rank_column = rank_column
    
    from typing import Any

    def generate_model_ratings(self,
        incoming_inference_features_str: str
        ) -> str:
        inference_dataframe = pl.DataFrame(json.loads(incoming_inference_features_str))
        inference_dataframe = inference_dataframe.with_column(
            pl.col("session_id").str.replace("-","").alias(f"{self.group_column}_hashed").hash(seed=0)
        )

        incoming_features = inference_dataframe.columns
        expected_features = lgb_model.feature_name()
        pred_label = "label" # EXPLAIN: does not matter here, we only construct rating
        assert all(expected_column == actual_column for expected_column, actual_column in zip(incoming_features, expected_features)),\
            "the inference feature do not have the same order as the training features, this can lead to poorer performance"
        inference_dataframe_pd = inference_dataframe.sort(
            by=[group_column, rank_column], reverse=False
        ).to_pandas()
        inference_dataframe_pd[pred_label] = self.model.predict(inference_dataframe_pd)
        inference_dataframe_pd[predicted_rank_column] = (
            inference_dataframe_pd.groupby(group_column)[pred_label]
            .rank(method="first", ascending=False)
        )
        predictions_pl = pl.DataFrame(inference_dataframe_pd)
        return predictions_pl.groupby('venue_id').agg(
        [
            pl.col(predicted_rank_column).quantile(0.8).alias(f"q80_{predicted_rank_column}")]
        ).select("venue_id", f"q80_{predicted_rank_column}").to_pandas().head(5).to_json(orient='records')


if __name__ == '__main__':
    ModelInstance(model_artifact_bucket="../../rate_venues.pickle")    

            
            
