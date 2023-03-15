from fastapi import Query
from pydantic import BaseModel


class SearchParameters(BaseModel):
    lat: float = Query(..., description="The latitude of the search location.")
    lon: float = Query(..., description="The longitude of the search location.")
