from fastapi import FastAPI

from .model import ModelInstance


class RankingInferenceServer:
    def __init__(
        self, model_name: str, model_artifact_bucket: str, group_column: str, rank_column: str
    ):
        self.ranking_model_name = model_name
        self.app = FastAPI()
        self.ranking_model = ModelInstance(
            model_artifact_bucket=model_artifact_bucket,
            group_column=group_column,
            rank_column=rank_column,
        )

        @self.app.post("/predict")
        # trunk-ignore(mypy/no-untyped-def)
        async def predict(self, incoming_inference_features: str) -> str:  # type: ignore
            return str(
                self.ranking_model.generate_model_ratings(
                    incoming_inference_features_str=incoming_inference_features
                )
            )
