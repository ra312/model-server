from pydantic import BaseModel, Field


class RestaurantDetails(BaseModel):
    venue_id: str = Field(
        "3188aa02-181c-11eb-8dc0-6e2275755fbc",
        description="ID of the venue being recommended",
        example=4202398962129790175,
    )
    image_url: str = Field(
        "https://discovery-cdn.wolt.com/categories/3188aa02-181c-11eb-8dc0-6e2275755fbc_8b140e11_cbed_4f92_bfa2_a85fc92d1249.jpg-md",
        description="URL to venue id products",
        example="https://discovery-cdn.wolt.com/categories/3188aa02-181c-11eb-8dc0-6e2275755fbc_8b140e11_cbed_4f92_bfa2_a85fc92d1249.jpg-md",
    )
