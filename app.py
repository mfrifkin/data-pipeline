# app.py
import streamlit as st
from pymongo import MongoClient
import pandas as pd

st.title("Daily NYC Weather Forecast")

client = MongoClient("mongodb+srv://mrifkin_db_user:I0uHXt05wtWA5t7x@cluster0.bfmieps.mongodb.net/?appName=Cluster0")
db = client.project_data
collection = db.weather

# Get the most recent document
latest = list(collection.find().sort("timestamp", -1).limit(1))[0]["data"]

# Convert to DataFrame and visualize
df = pd.DataFrame(latest)
st.dataframe(df)
st.line_chart(df["temperature_2m_max"])