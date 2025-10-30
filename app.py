import streamlit as st
from pymongo import MongoClient
import pandas as pd

# ----- PAGE CONFIG -----
st.set_page_config(
    page_title="NYC Weather Dashboard",
    page_icon="🌤️",
    layout="wide"
)

st.title("🌤️ NYC Daily Weather Forecast")

# ----- CONNECT TO MONGODB -----
# Replace with your actual connection URI
# client = MongoClient("mongodb+srv://mrifkin_db_user:I0uHXt05wtWA5t7x@cluster0.bfmieps.mongodb.net/project_data?appName=Cluster0")
client = MongoClient("mongodb+srv://mrifkin_db_user:I0uHXt05wtWA5t7x@cluster0.bfmieps.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true")
db = client.project_data
collection = db.weather

# ----- FETCH THE MOST RECENT DATASET -----
latest_doc = list(collection.find().sort("timestamp", -1).limit(1))[0]
data = latest_doc["data"]

# Convert to DataFrame
df = pd.DataFrame(data)

# ----- CLEAN & FORMAT DATA -----
df = df.rename(columns={"temperature_2m_max": "Max Temp (°C)", "time": "Date"})
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# ----- UNIT TOGGLE -----
unit = st.radio("Temperature Unit", ["°C", "°F"], horizontal=True)

if unit == "°F":
    df["Max Temp (°F)"] = df["Max Temp (°C)"] * 9/5 + 32
    plot_col = "Max Temp (°F)"
else:
    plot_col = "Max Temp (°C)"

# ----- METRICS -----
if unit == "°F":
    avg_val = df["Max Temp (°C)"].mean() * 9/5 + 32
    high_val = df["Max Temp (°C)"].max() * 9/5 + 32
    low_val  = df["Max Temp (°C)"].min() * 9/5 + 32
    suffix = "°F"
else:
    avg_val = df["Max Temp (°C)"].mean()
    high_val = df["Max Temp (°C)"].max()
    low_val  = df["Max Temp (°C)"].min()
    suffix = "°C"

col1, col2, col3 = st.columns(3)
col1.metric("Average", f"{avg_val:.1f} {suffix}")
col2.metric("High", f"{high_val:.1f} {suffix}")
col3.metric("Low", f"{low_val:.1f} {suffix}")

# ----- CHART -----
st.markdown("### 📈 Temperature Over Time")
st.line_chart(df.set_index("Date")[plot_col])

# ----- RAW DATA TABLE -----
with st.expander("Show raw data table"):
    st.dataframe(df)

# ----- LAST UPDATED -----
last_updated = latest_doc["timestamp"]
st.caption(f"Last updated: {last_updated.strftime('%B %d, %Y at %I:%M %p')}")

# ----- FOOTER -----
st.markdown("---")
st.markdown("Built with [Streamlit](https://streamlit.io/) · Data from [Open-Meteo API](https://open-meteo.com/)")