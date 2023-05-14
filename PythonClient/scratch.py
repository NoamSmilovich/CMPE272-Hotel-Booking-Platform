import pymongo
from datetime import datetime

client = pymongo.MongoClient("mongodb+srv://test-user:55555@cluster0.niruk0p.mongodb.net/?retryWrites=true&w=majority")
db = client["hotels_db"]
collection = db["hotels"]
collection.drop()

db = client["hotels_db"]
collection = db["hotels"]

hotels = [
    {
        "name": "The Grand Hotel",
        "address": "123 Main St",
        "city": "New York",
        "country": "USA",
        "phone": "+1-212-555-1234",
        "rating": 4.5,
        "amenities": {
            "pool": True,
            "gym": True,
            "spa": True,
            "restaurants": ["Italian", "French", "Japanese"],
        },
    },
    {
        "name": "The Ritz-Carlton",
        "address": "1 Central Park West",
        "city": "New York",
        "country": "USA",
        "phone": "+1-212-555-5678",
        "rating": 5.0,
        "amenities": {
            "pool": True,
            "gym": True,
            "spa": True,
            "restaurants": ["American", "French", "Seafood"],
        },
    },
    {
        "name": "The Plaza",
        "address": "768 5th Ave",
        "city": "New York",
        "country": "USA",
        "phone": "+1-212-555-9100",
        "rating": 4.0,
        "amenities": {
            "pool": False,
            "gym": True,
            "spa": True,
            "restaurants": ["European", "Asian"],
        },
    },
    {
        "name": "The Mandarin Oriental",
        "address": "80 Columbus Cir",
        "city": "New York",
        "country": "USA",
        "phone": "+1-212-555-4321",
        "rating": 4.8,
        "amenities": {
            "pool": True,
            "gym": True,
            "spa": True,
            "restaurants": ["Chinese", "French", "Japanese"],
        },
        "rooms": {
            "deluxe": {
                "description": "Spacious room with a king-size bed and a view of Central Park",
                "price": 600,
            },
            "suite": {
                "description": "Luxurious suite with a separate living area, dining table, and view of the city skyline",
                "price": 1200,
            },
        },
        "events": {
            "weddings": True,
            "conferences": True,
            "banquets": True,
            "capacity": 300,
        },
    },
    {
        "name": "The Fairmont",
        "address": "950 Mason St",
        "city": "San Francisco",
        "country": "USA",
        "phone": "+1-415-555-1234",
        "rating": 4.3,
        "amenities": {
            "pool": True,
            "gym": True,
            "spa": False,
            "restaurants": ["American", "French", "Japanese"],
        },
        "rooms": {
            "standard": {
                "description": "Comfortable room with a queen-size bed and a view of the city",
                "price": 300,
            },
            "club": {
                "description": "Spacious room with access to the Fairmont Gold Lounge and a view of the bay",
                "price": 500,
            },
            "suite": {
                "description": "Luxurious suite with a separate living area, dining table, and a view of the Golden Gate Bridge",
                "price": 1000,
            },
        },
    },
]

result = collection.insert_many(hotels)
print(f"Inserted {len(result.inserted_ids)} hotel documents")


db.grand_hotel_reservations.drop()
hotels_collection = db["hotels"]

# get the Grand Hotel document from the hotels collection
grand_hotel = hotels_collection.find_one({"name": "The Grand Hotel"})

# create a new collection for reservations for the Grand Hotel
reservations_collection = db.grand_hotel_reservations

# create some sample reservations for the Grand Hotel
reservations = [
    {"guest_name": "John Doe", "checkin_date": datetime(2023, 4, 25), "checkout_date": datetime(2023, 4, 30), "room_type": "Deluxe Room"},
    {"guest_name": "Jane Smith", "checkin_date": datetime(2023, 5, 1), "checkout_date": datetime(2023, 5, 5), "room_type": "Standard Room"},
    {"guest_name": "Alice Lee", "checkin_date": datetime(2023, 5, 10), "checkout_date": datetime(2023, 5, 15), "room_type": "Suite"},
    {"guest_name": "Bob Johnson", "checkin_date": datetime(2023, 5, 20), "checkout_date": datetime(2023, 5, 23), "room_type": "Deluxe Room"},
    {"guest_name": "Samantha Brown", "checkin_date": datetime(2023, 6, 1), "checkout_date": datetime(2023, 6, 5), "room_type": "Standard Room"},
    {"guest_name": "David Kim", "checkin_date": datetime(2023, 6, 10), "checkout_date": datetime(2023, 6, 15), "room_type": "Deluxe Room"},
    {"guest_name": "Maria Perez", "checkin_date": datetime(2023, 6, 20), "checkout_date": datetime(2023, 6, 22), "room_type": "Suite"},
    {"guest_name": "Alex Wong", "checkin_date": datetime(2023, 6, 25), "checkout_date": datetime(2023, 6, 30), "room_type": "Standard Room"}
]

# add the hotel reference to each reservation document
for reservation in reservations:
    reservation["hotel_id"] = grand_hotel["_id"]

# insert the reservations into the reservations collection
result = reservations_collection.insert_many(reservations)
print(f"Inserted {len(result.inserted_ids)} reservation documents")