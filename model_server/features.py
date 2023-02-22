from pydantic import BaseModel, Field


class InferenceFeatures(BaseModel):
    venue_id: int = Field(-4202398962129790175)
    conversions_per_impression: float = Field(0.3556765815)
    price_range: int = Field(1)
    rating: float = Field(8.6)
    popularity: float = Field(4.4884057024)
    retention_rate: float = Field(8.6)
    session_id_hashed: int = Field(3352618370338455358)
    position_in_list: int = Field(31)
    is_from_order_again: int = Field(0)
    is_recommended: int = Field(0)
