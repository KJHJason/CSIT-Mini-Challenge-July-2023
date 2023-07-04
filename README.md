# CSIT Mini Challenge #3: Software Engineering

## Summary

Mini Challenge: Help Mighty Saver Rabbit!
Mighty Saver Rabbit is trying to find the best travel deals across the internet for his friends. Will you help him solve this with some savvy backend development tricks?

[Start your challenge here!](https://go.gov.sg/se-minichallenge)
This Mini Challenge on Backend Development is open from 4 July to 23 July 2023.

## Mini Challenge Description

Mighty Saver Rabbit needs your help!
As a travel enthusiast, Mighty Saver Rabbit is on the lookout for the cheapest flights and hotels for an upcoming trip with his friends.

Due to his extensive research, he had a plethora of information scattered across his computer, notebook, and smartphone. He needed a way to consolidate the data and make it accessible to his friends so that they can decide on the flight and accommodation for their trip.

To solve this problem, Mighty Saver Rabbit decided to populate all the information into a database for consolidation. However, he still needs YOUR help to make the information accessible to his friends.

Follow the instructions below to complete the challenge and help Mighty Saver Rabbit!

## Instructions

On some paper and pen, Mighty Saver Rabbit eagerly scribbled down his idea:

![API Diagram](/res/Diagram.png)

You will build a REST API server, using any programming language of your choice (Python, Ruby, Typescript, to name a few...). Choose something you're comfortable with, or use this opportunity to challenge yourself with a new programming language - that's up to you!

Use the following connection address to connect to Mighty Saver Rabbit's MongoDB:

`mongodb+srv://userReadOnly:7ZT817O8ejDfhnBM@minichallenge.q4nve1r.mongodb.net/`

You can use [MongoDB Compass](https://www.mongodb.com/products/compass) to view the data directly.

On your API server, you should write two endpoints for Mighty Saver Rabbit's friends to query the following routes...

## GET /flight

Get a list of return flights at the cheapest price, given the destination city, departure date, and arrival date.

Query Parameters:

Field          | Type   | Description
-------------- | ------ | -------------------------------------------------
departureDate  | String | Departure date from Singapore (ISO date format).
returnDate     | String | Return date from destination city (ISO date format).
destination    | String | Destination city (case-insensitive).

Responses:

Status Code | Description
----------- | -----------------------------------------
200         | Query successful.
400         | Bad input. Missing query parameters or incorrect date format.

Response Format:

Returns an array containing the details of the cheapest return flights. There can be 0 or more items returned.

Example Query:

`/flight?departureDate=2023-12-10&returnDate=2023-12-16&destination=Frankfurt`

Example Response:

```json
[
  {
    "City": "Frankfurt",
    "Departure Date": "2023-12-10",
    "Departure Airline": "US Airways",
    "Departure Price": 1766,
    "Return Date": "2023-12-16",
    "Return Airline": "US Airways",
    "Return Price": 716
  }
]
```

## GET /hotel

Get a list of hotels providing the cheapest price, given the destination city, check-in date, and check-out date.

Query Parameters:

Field          | Type   | Description
-------------- | ------ | -------------------------------------------------
checkInDate    | String | Date of check-in at the hotel.
checkOutDate   | String | Date of check-out from the hotel.
destination    | String | Destination city (case-insensitive).

Responses:

Status Code | Description
----------- | -----------------------------------------
200         | Query successful.
400         | Bad input. Missing query parameters or incorrect date format.

Response Format:

Returns an array containing the details of the cheapest hotels. There can be 0 or more items returned.

Example Query:

`/hotel?checkInDate=2023-12-10&checkOutDate=2023-12-16&destination=Frankfurt`

Example Response:

```json
[
  {
    "City": "Frankfurt",
    "Check In Date": "2023-12-10",
    "Check Out Date": "2023-12-16",
    "Hotel": "Hotel J",
    "Price": 2959
  }
]
```

## Important Note

For your API server to be verified after submission, please run your server on port 8080

## Proof of Completion

![Proof of Completion](/res/proof.png)
