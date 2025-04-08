import streamlit as st
import pandas as pd

# Load dataset
df = pd.read_csv("final.csv")
df['Entrance Fee in INR'] = pd.to_numeric(df['Entrance Fee in INR'], errors='coerce')
df = df.dropna(subset=['Entrance Fee in INR'])

# Helper to get nearby places in the same city
def find_nearby_by_city(place_row, df_all, top_n=3):
    city = place_row['City']
    nearby = df_all[(df_all['City'] == city) & (df_all['Name'] != place_row['Name'])]
    return nearby.head(top_n)[['Name', 'Type', 'Google review rating']]

# Recommendation function
def recommend_destinations(zone=None, type=None, max_fee=None, dslr_allowed=None, include_nearby=False):
    filtered = df.copy()

    if zone:
        filtered = filtered[filtered['Zone'] == zone]
    if type:
        filtered = filtered[filtered['Type'].str.contains(type, case=False)]
    if max_fee is not None:
        filtered = filtered[filtered['Entrance Fee in INR'] <= max_fee]
    if dslr_allowed:
        filtered = filtered[filtered['DSLR Allowed'] == dslr_allowed]

    results = []
    for _, row in filtered.iterrows():
        entry = {
            'Name': row['Name'],
            'City': row['City'],
            'Google review rating': row['Google review rating'],
            'Entrance Fee in INR': row['Entrance Fee in INR'],
            'Best Time to visit': row['Best Time to visit']
        }

        if include_nearby:
            nearby = find_nearby_by_city(row, df)
            entry['Nearby Places'] = nearby.to_dict(orient='records')

        results.append(entry)

    return results

# ------------------ Streamlit App ------------------

st.set_page_config(page_title="Travel Destination Recommender", layout="wide")
st.title("🌍 Travel Destination Recommender")

# Sidebar for user input
st.sidebar.header("🔍 Filter your preferences")

zone = st.sidebar.selectbox("Select Zone", options=[""] + sorted(df['Zone'].dropna().unique().tolist()))
type_ = st.sidebar.selectbox("Select Type", options=[""] + sorted(df['Type'].dropna().unique().tolist()))
max_fee = st.sidebar.slider("Maximum Entrance Fee (INR)", min_value=0, max_value=1000, value=100)
dslr_allowed = st.sidebar.selectbox("DSLR Allowed?", options=["", "Yes", "No"])
include_nearby = st.sidebar.checkbox("Show Nearby Places", value=True)

if st.sidebar.button("🚀 Show Recommendations"):
    with st.spinner("Finding the best places for you..."):
        results = recommend_destinations(
            zone=zone if zone else None,
            type=type_ if type_ else None,
            max_fee=max_fee,
            dslr_allowed=dslr_allowed if dslr_allowed else None,
            include_nearby=include_nearby
        )

    if not results:
        st.warning("No matching destinations found. Try adjusting the filters.")
    else:
        for r in results:
            st.subheader(f"📍 {r['Name']} — {r['City']}")
            st.markdown(f"⭐ **Rating:** {r['Google review rating']} &nbsp;&nbsp;&nbsp; 💰 **Fee:** ₹{r['Entrance Fee in INR']}")
            st.markdown(f"🕰️ **Best Time to Visit:** {r['Best Time to visit']}")

            if include_nearby and 'Nearby Places' in r:
                with st.expander("🔎 Nearby Places in Same City"):
                    for n in r['Nearby Places']:
                        st.markdown(f"• **{n['Name']}** ({n['Type']}) — ⭐ {n['Google review rating']}")

            st.markdown("---")
