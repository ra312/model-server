# It's a class that creates a Flask app and allows you to add endpoints to it
from fastapi import FastAPI
from fastapi import APIRouter
import uvicorn


class InferenceServer:

    def __init__(self, name: str):
        self.name = name
        self.app = FastAPI()
        self.router = APIRouter()
        self.router.add_api_route("/predict", self.predict, methods=["GET"])
        self.app.include_router(self.predict)

    def predict(self):
        return {"relevance_scores": self.name}


if __name__ == "__main__":
    server = InferenceServer(name="ChatGPT")
    uvicorn.run(server.app, host="localhost", port=8000)


# app = FastAPI()
# hello = Hello("World")
# app.include_router(hello.router)

# from typing import Any
# import logging

# logging.basicConfig(level=logging.DEBUG)


# class ModelServer:
#     """
#     The ModelServer class is a wrapper around Flask that allows you to easily add endpoints to your
#     """

#     def __init__(self, **configs: dict[str, Any]):
#         """
#         The function takes in a dictionary of configuration values and sets them as the configuration
#         values for the Flask application.

#         :param : **configs: dict[str, Any]** - This is a dictionary of configurations that will be
#         passed to the Flask app
#         :type : dict[str, Any]
#         """
#         self.app = FastAPI()
#         # self.configs(**configs)



#     def configs(self, **configs):
#         for config, value in configs.items():
#             self.app.config[config.upper()] = value

#     def add_endpoint(
#         self,
#         endpoint: str = "/predict",
#         endpoint_name=None,
#         handler=None,
#         methods=["GET"],
#     ):
#         """
#         > This function adds a new endpoint to the Flask app
#         :param endpoint: The url rule for the endpoint, defaults to /predict
#         :type endpoint: str (optional)
#         :param endpoint_name: The name of the endpoint
#         :param handler: The function that will be called when the endpoint is requested
#         :param methods: The HTTP methods that are allowed
#         """
#         self.app.add_url_rule(
#             rule=endpoint, endpoint=endpoint_name, view_func=handler, methods=methods
#         )

#     def run(self, **kwargs):
#         """
#         It runs the Flask app
#         :param : `host`: The hostname to listen on. Defaults to `127.0.0.1` (localhost). Set this to
#         `'0.0.0.0'` to have the server available externally as well
#         :type : dict[str, Any]
#         """
#         logging.info("RUNNING MODEL SERVER APP with: ", kwargs)
#         self.app.run(**kwargs)
