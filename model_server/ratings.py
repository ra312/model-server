"""
The `VenueRating` class is a Pydantic `BaseModel`
used to represent the predicted ranking of a venue
in a recommendation system
"""
from pydantic import BaseModel, Field


class VenueRating(BaseModel):
    """
    Represents the predicted ranking of a venue.

    Attributes:
    -----------
    venue_id : int
        The ID of the venue being rated.
    q80_predicted_rank : float
        The predicted ranking of the venue,
        as a 80-quantile of predicted rating
        for venue across available sessions
    """

    venue_id: int = Field(-4202398962129790175, description="The ID of the venue being rated.")
    q80_predicted_rank: float = Field(
        8.6,
        description="""The predicted ranking of the venue,
        as a 80 - quantile of predicted rating
        for venue across available sessions""",
    )
