from fastapi import (
    APIRouter, 
    Query,
)
import pymongo
import datetime
from .database import get_db_client
from .logic import (
    process_flight_results, 
    convert_date_to_datetime,
)
from .responses import (
    Flight,
    Hotel,
)

api_router = APIRouter(include_in_schema=True)
RESPONSES = {
    200: {"description": "Query successful."},
    400: {"description": "Bad Input"},
}

@api_router.get(
    path="/flight",
    description="Get a list of return flights at the cheapest price, given the destination city, departure date, and arrival date.",
    responses=RESPONSES,
    response_model=list[Flight],
)
async def get_flight(
    departureDate: datetime.date = Query(description="Departure date from Singapore. ISO date format (YYYY-MM-DD)."), 
    returnDate: datetime.date = Query(description="Return date from destination city. ISO date format (YYYY-MM-DD)."), 
    destination: str = Query(min_length=1, max_length=500, description="Destination city. Case-insensitive.")
):
    destination = destination.title()

    # Convert departureDate and returnDate to datetime objects for mongodb query
    departure_date = convert_date_to_datetime(departureDate)
    return_date = convert_date_to_datetime(returnDate)

    # Query the database for available flights on the departure date
    db = get_db_client()
    col = db["flights"]
    departure_flight_cur = col.find({
        "srccity": "Singapore",
        "destcity": destination,
        "date": departure_date
    })
    async with departure_flight_cur:
        departure_flights = await process_flight_results(
            cur=departure_flight_cur, 
            is_return_flights=False,
        )
    if len(departure_flights) == 0:
        return []

    # Query the database for available flights on the return date
    return_flight_cur = col.find({
        "srccity": destination,
        "destcity": "Singapore",
        "date": return_date
    })
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
    responses=RESPONSES,
    response_model=list[Hotel],
)
async def get_flight(
    checkInDate: datetime.date = Query(description="Date of check-in at the hotel. ISO date format (YYYY-MM-DD)."), 
    checkOutDate: datetime.date = Query(description="Date of check-out from the hotel. ISO date format (YYYY-MM-DD)."), 
    destination: str = Query(min_length=1, max_length=500, description="Destination city. Case-insensitive."),
):
    destination = destination.title()

    # Convert checkInDate and checkOutDate to datetime objects for mongodb query
    chk_in_date = convert_date_to_datetime(checkInDate)
    chk_out_date = convert_date_to_datetime(checkOutDate)

    db = get_db_client()
    col = db["hotels"]

    # sacrifice space complexity for O(n) time complexity
    hotel_map: dict[str, list[dict]] = {}
    invalid_hotels: set[str] = set()
    hotel_price_map: dict[str, int] = {}

    # Query the database for available hotels between the check-in date and check-out date
    hotels_cur = col.find({
        "city": destination,
        "date": {
            "$gte": chk_in_date,
            "$lte": chk_out_date
        },
    })
    async with hotels_cur:
        hotels_cur = hotels_cur.sort("date", pymongo.ASCENDING)
        async for hotel in hotels_cur:
            hotel_name: str = hotel["hotelName"]
            if hotel_name in invalid_hotels:
                continue

            if hotel_name not in hotel_map:
                if hotel["date"] != chk_in_date:
                    invalid_hotels.add(hotel_name)

                hotel_map[hotel_name] = [hotel]
                hotel_price_map[hotel_name] = hotel["price"]
                continue

            # check the previous hotel in the list if there's a continuous date
            previous_idx = len(hotel_map[hotel_name]) - 1
            prev_hotel = hotel_map[hotel_name][previous_idx]
            if prev_hotel["date"] + datetime.timedelta(days=1) != hotel["date"]:
                invalid_hotels.add(hotel_name)
                continue

            # valid hotel, update the price and append to the list
            hotel_price_map[hotel_name] += hotel["price"]
            hotel_map[hotel_name].append(hotel)

    if len(hotel_price_map) == 0:
        return []

    # check for invalid hotels that does not reach the check-out date
    for hotel_name, hotel_list in hotel_map.items():
        if hotel_name not in invalid_hotels and len(hotel_list) < (chk_out_date - chk_in_date).days + 1:
            invalid_hotels.add(hotel_name)

    cheapest_hotel_price = min(hotel_price_map.values())
    chk_in_date_str = chk_in_date.strftime("%Y-%m-%d")
    chk_out_date_str = chk_out_date.strftime("%Y-%m-%d")
    return [
        {
            "City": "Frankfurt",
            "Check In Date": chk_in_date_str,
            "Check Out Date": chk_out_date_str,
            "Hotel": hotel_name,
            "Price": price,
        }
        for hotel_name, price in hotel_price_map.items() if price == cheapest_hotel_price and hotel_name not in invalid_hotels
    ]
