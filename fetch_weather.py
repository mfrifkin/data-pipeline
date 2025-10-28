from pymongo import MongoClient
import requests
from datetime import datetime

response = requests.get("https://api.open-meteo.com/v1/forecast?latitude=40.7&longitude=-74.0&daily=temperature_2m_max&timezone=America/New_York")
data = response.json()
print(data["daily"])
client = MongoClient("mongodb+srv://mrifkin_db_user:I0uHXt05wtWA5t7x@cluster0.bfmieps.mongodb.net/?appName=Cluster0")
db = client.project_data
collection = db.weather

# collection.insert_one({
#     "timestamp": datetime.now(),
#     "data": data["daily"]
# })

docs = list(collection.find())

# Print them out
for doc in docs:
    print(doc["data"])