import argparse

from .inference_server import model_endpoint


def parse_arguments() -> argparse.Namespace:
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

    # Parse arguments
    return parser.parse_args()


# Run the model endpoint with the specified arguments
args = parse_arguments()
model_endpoint(
    host=args.host, port=args.port, recommendation_model_path=args.recommendation_model_path
)
