from fastapi import (
    APIRouter, 
    Query,
)
import datetime
from .database import get_db_client
from .logic import (
    process_flight_results, 
    convert_date_to_datetime,
)

api_router = APIRouter(include_in_schema=True)

@api_router.get(
    path="/flight",
    description="Get a list of return flights at the cheapest price, given the destination city, departure date, and arrival date.",
)
async def get_flight(
    departureDate: datetime.date = Query(description="Departure date from Singapore.\nISO date format (YYYY-MM-DD)."), 
    returnDate: datetime.date = Query(description="Return date from destination city.\nISO date format (YYYY-MM-DD)."), 
    destination: str = Query(min_length=1, max_length=500, description="Destination city.\nCase-insensitive.")
):
    destination = destination.title()

    # Convert departureDate and returnDate to datetime objects for mongodb query
    departure_date = convert_date_to_datetime(departureDate)
    return_date = convert_date_to_datetime(returnDate)

    # Query the database for available flights on the departure date
    db = get_db_client()
    col = db["flights"]
    departure_flight_cur = col.find(
        {
            "srccity": "Singapore",
            "destcity": destination,
            "date": departure_date
        }
    )
    async with departure_flight_cur:
        departure_flights = await process_flight_results(
            cur=departure_flight_cur, 
            is_return_flights=False,
        )
    if len(departure_flights) == 0:
        return []

    # Query the database for available flights on the return date
    return_flight_cur = col.find(
        {
            "srccity": destination,
            "destcity": "Singapore",
            "date": return_date
        }
    )
    async with return_flight_cur:
        return_flights = await process_flight_results(
            cur=return_flight_cur, 
            is_return_flights=True,
        )
    if len(return_flights) == 0:
        return []

    departure_date: str = departure_date.strftime("%Y-%m-%d")
    return_date: str = return_date.strftime("%Y-%m-%d")
    return [
        {
            "City": destination,
            "Departure Date": departure_date,
            "Departure Airline": departure_flight["airlinename"],
            "Departure Price": departure_flight["price"],
            "Return Date": return_date,
            "Return Airline": return_flight["airlinename"],
            "Return Price": return_flight["price"]
        } for departure_flight, return_flight in zip(departure_flights, return_flights, strict=False)
    ]

@api_router.get(
    path="/hotel",
    description="Get a list of hotels providing the cheapest price, given the destination city, check-in date, and check-out date.",
)
async def get_flight(
    checkInDate: datetime.date = Query(description="Date of check-in at the hotel.\nISO date format (YYYY-MM-DD)."), 
    checkOutDate: datetime.date = Query(description="Date of check-out from the hotel.\nISO date format (YYYY-MM-DD)."), 
    destination: str = Query(min_length=1, max_length=500, description="Destination city.\nCase-insensitive.")
):
    destination = destination.title()

    # Convert checkInDate and checkOutDate to datetime objects for mongodb query
    chk_in_date = convert_date_to_datetime(checkInDate)
    chk_out_date = convert_date_to_datetime(checkOutDate)

    db = get_db_client()
    col = db["hotels"]
