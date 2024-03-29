import json

import polars as pl

from recommendation_model_server.model import ModelInstance


def test_model_prediction_routine() -> None:
    model = ModelInstance(
        model_artifact_bucket="artifacts/rate_venues.pickle",
        group_column="session_id",
        rank_column="rating",
    )
    test_incoming_inference_features = """[
        {"venue_id":-4202398962129790175,"conversions_per_impression":0.3556765815,"price_range":1,"rating":8.6,"popularity":4.4884057024,"retention_rate":0.5884095,"session_id_hashed":3352618370338455358,"position_in_list":0,"is_from_order_again":1,"is_recommended":0},
        {"venue_id":-8608196287932575311,"conversions_per_impression":0.1206581353,"price_range":1,"rating":9.2,"popularity":0.2022771056,"retention_rate":0.18,"session_id_hashed":4664838061955502305,"position_in_list":0,"is_from_order_again":0,"is_recommended":0},
        {"venue_id":-4202398962129790175,"conversions_per_impression":0.3556765815,"price_range":1,"rating":8.6,"popularity":4.4884057024,"retention_rate":0.5884095,"session_id_hashed":1006495267592422768,"position_in_list":0,"is_from_order_again":0,"is_recommended":0},
        {"venue_id":-4202398962129790175,"conversions_per_impression":0.3556765815,"price_range":1,"rating":8.6,"popularity":4.4884057024,"retention_rate":0.5884095,"session_id_hashed":16271107337218474123,"position_in_list":31,"is_from_order_again":0,"is_recommended":0},
        {"venue_id":-4202398962129790175,"conversions_per_impression":0.3556765815,"price_range":1,"rating":8.6,"popularity":4.4884057024,"retention_rate":0.5884095,"session_id_hashed":12992628493413309367,"position_in_list":0,"is_from_order_again":1,"is_recommended":0},
        {"venue_id":8968794542286256815,"conversions_per_impression":0.4036363636,"price_range":1,"rating":8.8,"popularity":0.8977682883,"retention_rate":0.272727,"session_id_hashed":11792925231034451836,"position_in_list":13,"is_from_order_again":1,"is_recommended":1},
        {"venue_id":-4202398962129790175,"conversions_per_impression":0.3556765815,"price_range":1,"rating":8.6,"popularity":4.4884057024,"retention_rate":0.5884095,"session_id_hashed":2327279187342959944,"position_in_list":0,"is_from_order_again":1,"is_recommended":0},
        {"venue_id":-4202398962129790175,"conversions_per_impression":0.3556765815,"price_range":1,"rating":8.6,"popularity":4.4884057024,"retention_rate":0.5884095,"session_id_hashed":6669153405411707628,"position_in_list":33,"is_from_order_again":1,"is_recommended":0},
        {"venue_id":8968794542286256815,"conversions_per_impression":0.4036363636,"price_range":1,"rating":8.8,"popularity":0.8977682883,"retention_rate":0.272727,"session_id_hashed":3159537071444654512,"position_in_list":5,"is_from_order_again":0,"is_recommended":0},
        {"venue_id":8968794542286256815,"conversions_per_impression":0.4036363636,"price_range":1,"rating":8.8,"popularity":0.8977682883,"retention_rate":0.272727,"session_id_hashed":13008284017370400506,"position_in_list":31,"is_from_order_again":1,"is_recommended":1}
        ]""".replace(
        "\n", ""
    ).replace(
        " ", ""
    )
    test_inference_dataframe = pl.DataFrame(json.loads(test_incoming_inference_features))
    expected_response = [
        {"venue_id": -8608196287932575311, "q80_predicted_rank": 1.0},
        {"venue_id": -4202398962129790175, "q80_predicted_rank": 1.0},
        {"venue_id": 8968794542286256815, "q80_predicted_rank": 1.0},
    ]
    generated_response = model.generate_model_ratings(inference_dataframe=test_inference_dataframe)
    assert generated_response == expected_response
