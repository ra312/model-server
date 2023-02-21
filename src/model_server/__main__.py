import uvicorn

from .inference_server import RankingInferenceServer

server = RankingInferenceServer(
    model_name="recommend-venues",
    model_artifact_bucket="/workspaces/model-server/rate_venues.pickle",
    group_column="session_id",
    rank_column="rating",
)
uvicorn.run(server.app, host="0.0.0.0", port=8080)
