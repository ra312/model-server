# It's a class that creates a Flask app and allows you to add endpoints to it
from typing import Dict

from fastapi import APIRouter, FastAPI


class InferenceServer:
    def __init__(self, name: str):
        self.name = name
        self.app = FastAPI()
        self.router = APIRouter()
        self.router.add_api_route("/predict", self.predict, methods=["GET"])
        self.app.include_router(self.router)

    def predict(self) -> Dict[str, str]:

        return {"relevance_scores": self.name}


# if __name__ == "__main__":
#     server = InferenceServer(name="recommend-venues")
#     uvicorn.run(server.app, host="localhost", port=8000)
