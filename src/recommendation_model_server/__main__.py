"""
This module provides a command-line interface
to run a model endpoint with specified host, port,
and trained model path.

It uses the argparse module to
parse command-line arguments and
calls the `model_endpoint` function
from the `inference_server`
module to start the model server.
"""

import argparse

import uvicorn
from fastapi import FastAPI

from .recommendation_api import create_recommendation_api
from .utils import declare_env_variables


def parse_arguments() -> argparse.Namespace:
    """Parse command-line arguments and return an `argparse.Namespace` object.

    Returns:
        argparse.Namespace: An object containing the parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(
        description="Specify host, port, and trained model bucket path."
    )

    # Add arguments
    parser.add_argument(
        "--host", type=str, default="localhost", help="the host to connect to (default: localhost)"
    )
    parser.add_argument(
        "--port", type=int, default=8080, help="the port to connect to (default: 8080)"
    )
    parser.add_argument(
        "--recommendation-model-path",
        type=str,
        required=True,
        help="the S3 bucket path for the trained model",
    )
    return parser.parse_args()


def entrypoint(parsed_args: argparse.Namespace) -> FastAPI:
    """Start the model endpoint with the specified host, port, and trained model path.

    Args:
        host (str): The host to connect to.
        port (int): The port to connect to.
        recommendation_model_path (str): The S3 bucket path for the trained model.
    """

    # Run the model endpoint with the specified arguments
    api: FastAPI = create_recommendation_api(
        recommendation_model_path=parsed_args.recommendation_model_path,
    )
    return api


if __name__ == "__main__":
    parsed_arguments = parse_arguments()
    declare_env_variables(parsed_arguments)
    app: FastAPI = entrypoint(parsed_arguments)
    uvicorn.run(app, host=parsed_arguments.host, port=parsed_arguments.port)
