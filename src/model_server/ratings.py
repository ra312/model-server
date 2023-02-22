from pydantic import BaseModel, Field


class VenueRating(BaseModel):
    venue_id: int = Field(-4202398962129790175)
    q80_predicted_rank: float = Field(8.6)
