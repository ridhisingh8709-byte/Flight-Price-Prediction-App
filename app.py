import streamlit as st
import pandas as pd
import joblib
from datetime import datetime

# Load trained model
model = joblib.load("flight_price_model.pkl")

# Page settings
st.set_page_config(
    page_title="Flight Price Prediction",
    page_icon="✈️"
)

st.title("✈️ Flight Price Prediction")
st.write("Enter flight details to predict the estimated ticket price.")

# Encoding mappings
airline_mapping = {
    "Trujet": 0,
    "SpiceJet": 1,
    "Air Asia": 2,
    "IndiGo": 3,
    "GoAir": 4,
    "Vistara": 5,
    "Vistara Premium economy": 6,
    "Air India": 7,
    "Multiple carriers": 8,
    "Multiple carriers Premium economy": 9,
    "Jet Airways": 10,
    "Jet Airways Business": 11
}

destination_mapping = {
    "Kolkata": 0,
    "Hyderabad": 1,
    "Delhi": 2,
    "Banglore": 3,
    "Cochin": 4
}

# User inputs
airline = st.selectbox(
    "Select Airline",
    list(airline_mapping.keys())
)

source = st.selectbox(
    "Select Source",
    ["Banglore", "Kolkata", "Delhi", "Chennai", "Mumbai"]
)

destination = st.selectbox(
    "Select Destination",
    list(destination_mapping.keys())
)

journey_date = st.date_input("Journey Date")

departure_time = st.time_input("Departure Time")

arrival_time = st.time_input("Arrival Time")

total_stops = st.selectbox(
    "Total Stops",
    [0, 1, 2, 3, 4]
)

duration_hours = st.number_input(
    "Duration Hours",
    min_value=0,
    max_value=50,
    value=2
)

duration_minutes = st.number_input(
    "Duration Minutes",
    min_value=0,
    max_value=59,
    value=30
)

if st.button("Predict Flight Price"):

    airline_encoded = airline_mapping[airline]
    destination_encoded = destination_mapping[destination]

    journey_day = journey_date.day
    journey_month = journey_date.month

    dep_hour = departure_time.hour
    dep_minute = departure_time.minute

    arrival_hour = arrival_time.hour
    arrival_minute = arrival_time.minute

    duration_hour = duration_hours
    duration_minute = duration_minutes
    duration_in_minute = duration_hour * 60 + duration_minute

    source_banglore = 1 if source == "Banglore" else 0
    source_kolkata = 1 if source == "Kolkata" else 0
    source_delhi = 1 if source == "Delhi" else 0
    source_chennai = 1 if source == "Chennai" else 0
    source_mumbai = 1 if source == "Mumbai" else 0

    input_data = pd.DataFrame([{
        "Airline": airline_encoded,
        "Destination": destination_encoded,
        "Total_Stops": total_stops,
        "Journey_day": journey_day,
        "Journey_month": journey_month,
        "Dep_Time_hour": dep_hour,
        "Dep_Time_minute": dep_minute,
        "Arrival_Time_hour": arrival_hour,
        "Arrival_Time_minute": arrival_minute,
        "Duration_hours": duration_hours,
        "Duration_mins": duration_minutes,
        "Duration_hour": duration_hour,
        "Duration_minute": duration_minute,
        "Duration_in_minute": duration_in_minute,
        "Source_Banglore": source_banglore,
        "Source_Kolkata": source_kolkata,
        "Source_Delhi": source_delhi,
        "Source_Chennai": source_chennai,
        "Source_Mumbai": source_mumbai
    }])

    prediction = model.predict(input_data)

    st.success(
        f"Estimated Flight Price: ₹{prediction[0]:,.2f}"
    )