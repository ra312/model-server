import json
import logging

import invokust
from locust import HttpUser, between, task

PERCENTAGE_OF_FAILED_REQUESTS = 1
MAX_RESPONSE_TIME_IN_MILLISECONDS = 20000
NUM_OF_USERS = int(1e6)
NUM_OF_NEW_USERS_PER_SECOND = 100


class RecommendationModelUser(HttpUser):
    wait_time = between(0, 5)

    @task
    def send_inference_request(self) -> None:

        request_body = {
            "venue_id": -4202398962129790000,
            "conversions_per_impression": 0.3556765815,
            "price_range": 1,
            "rating": 8.6,
            "popularity": 4.4884057024,
            "retention_rate": 8.6,
            "session_id_hashed": 3352618370338455600,
            "position_in_list": 31,
            "is_from_order_again": 0,
            "is_recommended": 0,
        }
        number_of_inference_requests = 1
        request_body_json = json.dumps([request_body] * number_of_inference_requests)
        request_body_bytes = request_body_json.encode()
        self.client.post("/predict", data=request_body_bytes)


def test_load_performance() -> None:
    """
    please start server locally by running
    'python3 -m recommendation_model_server \
        --host 0.0.0.0 \
        --port 8000 \
        --recommendation-model-path artifacts/rate_venues.pickle
    ',
    where file artifacts/rate_venues.pickle has to exist locally
    """
    settings = invokust.create_settings(
        classes=[RecommendationModelUser],
        host="http://0.0.0.0:8000",
        num_users=NUM_OF_USERS,
        spawn_rate=NUM_OF_NEW_USERS_PER_SECOND,
        run_time="10s",
    )

    loadtest = invokust.LocustLoadTest(settings)
    loadtest.run()
    test_stats = loadtest.stats()
    assert "num_requests_fail" in test_stats
    assert "num_requests" in test_stats
    actual_percentage_of_failed_requests = (
        test_stats["num_requests_fail"] / test_stats["num_requests"] * 100
    )
    logging.info("Percentage of failed requests %s", actual_percentage_of_failed_requests)
    assert actual_percentage_of_failed_requests <= PERCENTAGE_OF_FAILED_REQUESTS
    # pprint.pprint(test_stats, indent=4)

    assert (
        test_stats["requests"]["POST_/predict"]["max_response_time"]
        <= MAX_RESPONSE_TIME_IN_MILLISECONDS
    )


# async def start_server(app):
#     server = Process(target=uvicorn.run,
#                      args=(app,),
#                      kwargs={
#                          "host": "0.0.0.0",
#                          "port": 8000,
#                          "log_level": "info"},
#                      daemon=True)
#     server.start()
#     await asyncio.sleep(1)
#     return server


# async def tearDown(server):
#     """ Shutdown the app. """
#     server.terminate()


# def test_performance_results(app):
#     test_stats = generate_load_test_report()
#     assert "num_requests_fail" in test_stats
#     assert "num_requests" in test_stats
#     ACTUAL_PERCENTAGE_OF_FAILED_REQUESTS = (
#         test_stats["num_requests_fail"] / test_stats["num_requests"] * 100
#     )
#     logging.info("Percentage of failed requests %s",
#                  ACTUAL_PERCENTAGE_OF_FAILED_REQUESTS)
#     assert ACTUAL_PERCENTAGE_OF_FAILED_REQUESTS <= PERCENTAGE_OF_FAILED_REQUESTS
#     # pprint.pprint(test_stats, indent=4)

#     assert (
#         test_stats["requests"]["POST_/predict"]["max_response_time"]
#         <= MAX_RESPONSE_TIME_IN_MILLISECONDS
#     )
