"""
The InferenceFeatures class is a Pydantic BaseModel
that represents the features used for venue rating inference.
"""
from pydantic import BaseModel, Field


class InferenceFeatures(BaseModel):
    venue_id: int = Field(
        -4202398962129790175,
        description="ID of the venue being recommended",
        example=4202398962129790175,
    )
    conversions_per_impression: float = Field(
        0.3556765815,
        description="The average number of conversions per impression that the venue receives",
        example=0.678,
    )
    price_range: int = Field(
        1,
        description="Price range of the venue on a scale of 1-4",
        ge=1,
        le=4,
    )
    rating: float = Field(
        8.6,
        description="Rating of the venue on a scale of 1-10",
        ge=1,
        le=10,
    )
    popularity: float = Field(
        4.4884057024,
        description="The number of views or clicks per impression that the venue receives",
        example=3.45,
    )
    retention_rate: float = Field(
        8.6,
        description="The percentage of users who return to the app after viewing the venue",
        example=0.75,
    )
    session_id_hashed: int = Field(
        3352618370338455358,
        description="The hashed session ID of the user",
        example=1410427373869408199,
    )
    position_in_list: int = Field(
        31,
        description="The position of the venue in the recommended list",
        ge=1,
    )
    is_from_order_again: int = Field(
        0,
        description="Indicates whether the venue was ordered again by the user",
        example=1,
    )
    is_recommended: int = Field(
        0,
        description="Indicates whether the venue was recommended to the user",
        example=1,
    )
