# from model_server import InferenceServer


# import requests

# def test_predict():
#     server = InferenceServer(name="test-server")
#     data = [[1424193000929084737, 0.403492, 1, 8.6, 5.537811, 0.384965, 0, 1, 0],
#             [1424193000929084736, 0.403492, 1, 8.6, 5.537811, 0.384965, 0, 1, 0],
#             [1424193000929084735, 0.403492, 1, 8.6, 5.537811, 0.384965, 0, 1, 0],
#             [1424193000929084734, 0.403492, 1, 8.6, 5.537811, 0.384965, 0, 1, 0]]

#     real_response = requests.get("http://localhost:8000/predict", json=data)
#     expected_response = {
#     "venue_id": [1424193000929084737, 1424193000929084736, 1424193000929084735, 1424193000929084734],
#     "has_seen_venue_in_this_session": [0.0, 0.0, 0.0, 0.0]
#     }


# @app.get("/example")
# async def example():

#     return response
