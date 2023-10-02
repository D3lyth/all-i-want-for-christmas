import pymongo
from pymongo import MongoClient

# Connect to MongoDB

client = MongoClient(
    'mongodb+srv://d3lyth:H4rryP0tt3r@cluster0.prxun6h.mongodb.net/?retryWrites=true&w=majority')
db = client['all-i-want-for-christmas']
gifts_collection = db['gifts']

# Function to calculate the running total


def calculate_running_total():
    running_total = 0
    for gift in gifts_collection.find():
        running_total += gift['cost']
        gifts_collection.update_one({'_id': gift['_id']}, {
                                    '$set': {'running_total': running_total}})


if __name__ == "__main__":
    calculate_running_total()
