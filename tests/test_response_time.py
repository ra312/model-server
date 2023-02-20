import time

from fastapi.testclient import TestClient

from model_server import InferenceServer


def test_predict_latency() -> None:
    """
    Test the response time of a prediction endpoint in the InferenceServer class.

    The test sends a GET request to the '/predict' endpoint and measures the elapsed time.
    It asserts that the response is valid and that the elapsed time is less than or equal to 2.2 milliseconds.
    """
    # Create an instance of InferenceServer and a TestClient to interact with it
    app = InferenceServer(name="test-response-time")
    client = TestClient(app.app)

    # Send a GET request to the '/predict' endpoint and measure the elapsed time
    with client:
        start_time = time.monotonic()
        response = client.get("/predict")
        elapsed_time = time.monotonic() - start_time

        # Assert that the response is valid and the elapsed time is less than or equal to 2.2 milliseconds
        assert response.status_code == 200
        assert response.json() == {"relevance_scores": "test-response-time"}
        assert elapsed_time <= 0.004
        # NOTE: 0.0022 - time taken locally, 0.004 time taken in github actions
