import orjson
from pydantic import (
    BaseModel, 
    Field,
)
from fastapi.responses import ORJSONResponse

class Hotel(BaseModel):
    city: str = Field(
        alias="City",
    )
    check_in_date: str = Field(
        alias="Check In Date",
    )
    check_out_date: str = Field(
        alias="Check Out Date",
    )
    hotel: str = Field(
        alias="Hotel",
    )
    price: int = Field(
        alias="Price",
    )

class Flight(BaseModel):
    city: str = Field(
        alias="City",
    )
    departure_date: str = Field(
        alias="Departure Date",
    )
    departure_airline: str = Field(
        alias="Departure Airline",
    )
    departure_price: int = Field(
        alias="Departure Price",
    )
    return_date: str = Field(
        alias="Return Date",
    )
    return_airline: str = Field(
        alias="Return Airline",
    )
    return_price: int = Field(
        alias="Return Price",
    )

class Index(BaseModel):
    message: str
    author: str
    github: str
    api_routes: list[str]
    documentation_routes: list[str]

class PrettyORJSON(ORJSONResponse):
    """A modified version of the ORJSONResponse 
    class that returns an indented JSON response.
    """
    def render(self, content: dict[str, str]) -> bytes:
        return orjson.dumps(
            content, 
            option=orjson.OPT_NON_STR_KEYS | orjson.OPT_SERIALIZE_NUMPY | orjson.OPT_INDENT_2,
        )

