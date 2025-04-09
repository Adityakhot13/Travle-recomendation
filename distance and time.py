import streamlit as st
import pandas as pd
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler
from geopy.distance import geodesic
from geopy.geocoders import Nominatim

# ------------------ Distance & Cost Estimation ------------------ #
def get_coordinates(location_name):
    geolocator = Nominatim(user_agent="travel_app")
    location = geolocator.geocode(location_name)
    return (location.latitude, location.longitude) if location else None

def calculate_costs(distance_km):
    return {
        "Car (₹10/km)": round(distance_km * 10, 2),
        "Train (₹2/km)": round(distance_km * 2, 2),
        "Flight (₹6/km)": round(distance_km * 6, 2)
    }
# ------------------ Travel Cost Calculator ------------------ #
st.markdown("## 📌 Estimate Travel Distance and Cost")
with st.form("travel_form"):
    col1, col2 = st.columns(2)
    with col1:
        start_location = st.text_input("🛫 Enter Starting Location (e.g., Delhi)")
    with col2:
        end_location = st.text_input("🏁 Enter Destination Location (e.g., Agra)")
    calculate = st.form_submit_button("Calculate Distance & Travel Cost")

if calculate:
    start_coords = get_coordinates(start_location)
    end_coords = get_coordinates(end_location)

    if not start_coords or not end_coords:
        st.error("❌ Could not determine the location. Please check the names.")
    else:
        distance_km = geodesic(start_coords, end_coords).km
        cost_dict = calculate_costs(distance_km)

        st.success(f"📍 Distance between **{start_location}** and **{end_location}** is **{round(distance_km, 2)} km**.")
        st.markdown("### 💸 Estimated Travel Costs")
        for mode, cost in cost_dict.items():
            st.markdown(f"- **{mode}**: ₹{cost}")