import json
import logging
import time

from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_send_inference_request(app: FastAPI, request_body: dict) -> None:
    """
    Test the speed and request size of the model's inference.

    This test sends a POST request to the model's endpoint using a test client, with a request
    body containing a single JSON object. The elapsed time and request size in kilobytes are
    logged using the Python logging module. The test passes if the response status code is 200.

    To run this test, you need to have a running instance of the model endpoint.

    Example usage: `pytest -s test_inference_speed_and_request_size.py`

    Args:
        app (FastAPI): A FastAPI instance with a single endpoint for generating predicted venue ratings.
    """

    number_of_inference_requests = 100
    request_body_json = json.dumps([request_body] * number_of_inference_requests)
    request_body_bytes = request_body_json.encode()

    headers = {"accept": "application/json", "Content-Type": "application/json"}

    with TestClient(app) as client:
        start_time = time.monotonic()
        response = client.post("/predict", headers=headers, content=request_body_bytes)
        elapsed_time = time.monotonic() - start_time
        request_size_kb = len(request_body_bytes) / 1024
        logging.info("Number of inference requests: %s", number_of_inference_requests)
        logging.info(
            f"Request size: {request_size_kb:.2f} KB, Elapsed time: {elapsed_time:.4f} seconds"
        )
        assert 0.01 <= elapsed_time <= 0.031
        assert response.status_code == 200
