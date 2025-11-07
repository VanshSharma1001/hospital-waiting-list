import streamlit as st
import pandas as pd
import numpy as np

# ------------------------------------------
# Create Indian hospital dataset (local)
# ------------------------------------------
def create_hospital_data():
    np.random.seed(42)  # For reproducibility
    data = {
        "City": [
            "Delhi", "Delhi", "Mumbai", "Mumbai", "Chennai", "Chennai",
            "Kolkata", "Kolkata", "Bengaluru", "Bengaluru", "Hyderabad", "Hyderabad",
            "Pune", "Pune", "Ahmedabad", "Ahmedabad"
        ],
        "Hospital Name": [
            "AIIMS Delhi", "Fortis Escorts Heart Institute",
            "Lilavati Hospital", "Kokilaben Dhirubhai Ambani Hospital",
            "Apollo Hospitals Chennai", "Fortis Malar Hospital",
            "AMRI Hospitals Kolkata", "Fortis Hospital Anandapur",
            "Manipal Hospital Bengaluru", "Apollo Hospitals Bannerghatta",
            "Yashoda Hospitals Hyderabad", "Care Hospitals Banjara Hills",
            "Jehangir Hospital Pune", "Ruby Hall Clinic",
            "Sterling Hospital Ahmedabad", "Zydus Hospital Ahmedabad"
        ],
        "Department": [
            "Cardiology", "Neurology",
            "Orthopedics", "Cardiology",
            "Oncology", "Pediatrics",
            "Cardiology", "Orthopedics",
            "Neurology", "Cardiology",
            "Oncology", "Pediatrics",
            "Orthopedics", "Cardiology",
            "Neurology", "Oncology"
        ],
        # Simulate waiting times (in minutes)
        "Average Waiting Time (mins)": np.random.randint(10, 120, 16),
        # Simulate bed availability
        "Beds Available": np.random.randint(5, 80, 16)
    }
    return pd.DataFrame(data)

# Create hospital dataset
hospital_df = create_hospital_data()

# ------------------------------------------
# Streamlit App UI
# ------------------------------------------
st.set_page_config(page_title="Hospital Finder India", page_icon="🏥", layout="wide")
st.title("🏥 Hospital Finder — India 🇮🇳")

st.markdown(
    """
    This app helps patients find **hospitals in their city** and choose the one with the **shortest waiting time**.  
    Data is simulated locally using **Pandas** and **NumPy**.
    """
)

# ------------------------------------------
# Search Inputs
# ------------------------------------------
cities = sorted(hospital_df["City"].unique().tolist())
city_input = st.selectbox("Select Your City:", ["Select a City"] + cities)

departments = ["All"] + sorted(hospital_df["Department"].unique().tolist())
department_filter = st.selectbox("Select Department (optional):", departments)

# ------------------------------------------
# Search Logic
# ------------------------------------------
if city_input != "Select a City":
    # Filter by city
    region_filtered = hospital_df[hospital_df["City"] == city_input]

    # Filter by department if selected
    if department_filter != "All":
        region_filtered = region_filtered[region_filtered["Department"] == department_filter]

    if region_filtered.empty:
        st.warning("⚠️ No hospitals found for the selected city and department.")
    else:
        # Sort hospitals by waiting time
        region_sorted = region_filtered.sort_values(by="Average Waiting Time (mins)", ascending=True)

        st.subheader(f"🏙️ Hospitals in {city_input}")
        st.dataframe(region_sorted, use_container_width=True)

        # Highlight hospital with least waiting time
        best_hospital = region_sorted.iloc[0]
        st.success(
            f"✅ **Recommended Hospital:** {best_hospital['Hospital Name']}  "
            f"({best_hospital['Department']}) — Average Waiting Time: "
            f"**{best_hospital['Average Waiting Time (mins)']} mins**"
        )

        # Visualization
        st.bar_chart(
            data=region_sorted.set_index("Hospital Name")["Average Waiting Time (mins)"],
            use_container_width=True
        )
else:
    st.info("🔍 Please select a city to view hospitals.")

# ------------------------------------------
# Export Hospital Data
# ------------------------------------------
st.download_button(
    label="📥 Download Hospital Data (CSV)",
    data=hospital_df.to_csv(index=False).encode('utf-8'),
    file_name="hospital_data_india.csv",
    mime="text/csv"
)

st.caption("Built with ❤️ using Streamlit, Pandas, and NumPy — for the Indian healthcare ecosystem 🇮🇳.")
