import datetime
import pymongo
from pymongo.cursor import Cursor

async def process_flight_results(cur: Cursor, is_return_flights: bool) -> list[dict]:
    """Process the results from the database query and return a list of cheapest return flights."""
    cur = cur.sort("price", pymongo.ASCENDING)
    if not is_return_flights:
        return [flight async for flight in cur]

    results: list[dict] = []
    cheapest_flight = {}
    async for flight in cur:
        if len(results) == 0:
            cheapest_flight = flight
            results.append(flight)
        elif flight["price"] == cheapest_flight["price"] and flight["airlinename"] != cheapest_flight["airlinename"]:
            results.append(flight)
        else:
            break
    return results

def convert_date_to_datetime(date: datetime.date) -> datetime.datetime:
    return datetime.datetime.combine(date, datetime.datetime.min.time())
