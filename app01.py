import streamlit as st
import pandas as pd
import numpy as np

# ------------------------------------------
# Create Indian hospital dataset (local)
# ------------------------------------------
def create_hospital_data():
    np.random.seed(42)
    data = {
        "City": [
            # Delhi
            "Delhi", "Delhi",
            # Mumbai
            "Mumbai", "Mumbai",
            # Chennai
            "Chennai", "Chennai",
            # Kolkata
            "Kolkata", "Kolkata",
            # Bengaluru
            "Bengaluru", "Bengaluru",
            # Hyderabad
            "Hyderabad", "Hyderabad",
            # Pune
            "Pune", "Pune",
            # Ahmedabad
            "Ahmedabad", "Ahmedabad",
            # Gwalior
            "Gwalior", "Gwalior",
            # Jaipur
            "Jaipur", "Jaipur"
        ],
        "Hospital Name": [
            # Delhi
            "AIIMS Delhi", "Fortis Escorts Heart Institute",
            # Mumbai
            "Lilavati Hospital", "Kokilaben Dhirubhai Ambani Hospital",
            # Chennai
            "Apollo Hospitals Chennai", "Fortis Malar Hospital",
            # Kolkata
            "AMRI Hospitals Kolkata", "Fortis Hospital Anandapur",
            # Bengaluru
            "Manipal Hospital Bengaluru", "Apollo Hospitals Bannerghatta",
            # Hyderabad
            "Yashoda Hospitals Hyderabad", "Care Hospitals Banjara Hills",
            # Pune
            "Jehangir Hospital Pune", "Ruby Hall Clinic Pune",
            # Ahmedabad
            "Sterling Hospital Ahmedabad", "Zydus Hospital Ahmedabad",
            # Gwalior
            "Birla Hospital Gwalior", "Gajara Raja Medical College Hospital",
            # Jaipur
            "Fortis Escorts Hospital Jaipur", "SMS Hospital Jaipur"
        ],
        # Each hospital can now have multiple departments
        "Departments": [
            "Cardiology, Neurology, Orthopedics",
            "Cardiology, Oncology",
            "Orthopedics, Cardiology, Pediatrics",
            "Cardiology, Oncology, Neurology",
            "Oncology, Neurology, Pediatrics",
            "Cardiology, Orthopedics",
            "Cardiology, Orthopedics, Pediatrics",
            "Neurology, Oncology",
            "Neurology, Cardiology, Pediatrics",
            "Cardiology, Orthopedics, Oncology",
            "Oncology, Neurology",
            "Pediatrics, Orthopedics",
            "Orthopedics, Cardiology, Neurology",
            "Cardiology, Oncology, Pediatrics",
            "Neurology, Cardiology",
            "Oncology, Orthopedics",
            "Orthopedics, Pediatrics, Neurology",
            "Cardiology, Oncology",
            "Cardiology, Neurology, Pediatrics",
            "Oncology, Cardiology"
        ],
        # Simulate average waiting times (in minutes)
        "Average Waiting Time (mins)": np.random.randint(10, 120, 20),
        # Simulate available beds
        "Beds Available": np.random.randint(5, 80, 20)
    }

    return pd.DataFrame(data)

# Create dataset
hospital_df = create_hospital_data()

# ------------------------------------------
# Streamlit UI
# ------------------------------------------
st.set_page_config(page_title="Hospital Finder India", page_icon="🏥", layout="wide")
st.title("🏥 Hospital Finder — India 🇮🇳")

st.markdown(
    """
    This app helps patients find **hospitals in their city** and filter by **department**, showing the one with the **shortest waiting time**.  
    Data is simulated locally using **Pandas** and **NumPy**.
    """
)

# ------------------------------------------
# Search Inputs
# ------------------------------------------
cities = sorted(hospital_df["City"].unique().tolist())
city_input = st.selectbox("🏙️ Select Your City:", ["Select a City"] + cities)

# Create a list of all departments from all hospitals
unique_departments = sorted(
    list({d.strip() for dep_list in hospital_df["Departments"] for d in dep_list.split(",")})
)
department_filter = st.selectbox("🏥 Select Department (optional):", ["All"] + unique_departments)

# ------------------------------------------
# Search Logic
# ------------------------------------------
if city_input != "Select a City":
    # Filter hospitals by city
    region_filtered = hospital_df[hospital_df["City"] == city_input]

    # Filter by department (if selected)
    if department_filter != "All":
        region_filtered = region_filtered[
            region_filtered["Departments"].str.contains(department_filter, case=False, na=False)
        ]

    if region_filtered.empty:
        st.warning("⚠️ No hospitals found for the selected city and department.")
    else:
        # Sort hospitals by waiting time (ascending)
        region_sorted = region_filtered.sort_values(by="Average Waiting Time (mins)", ascending=True)

        st.subheader(f"🏙️ Hospitals in {city_input}")
        st.dataframe(region_sorted, use_container_width=True)

        # Highlight the best option
        best_hospital = region_sorted.iloc[0]
        st.success(
            f"✅ **Recommended Hospital:** {best_hospital['Hospital Name']} "
            f"— Departments: *{best_hospital['Departments']}*  \n"
            f"🕒 Average Waiting Time: **{best_hospital['Average Waiting Time (mins)']} mins**"
        )

        # Bar chart visualization
        st.bar_chart(
            data=region_sorted.set_index("Hospital Name")["Average Waiting Time (mins)"],
            use_container_width=True
        )
else:
    st.info("🔍 Please select a city to view available hospitals.")

# ------------------------------------------
# Export Data
# ------------------------------------------
st.download_button(
    label="📥 Download Hospital Data (CSV)",
    data=hospital_df.to_csv(index=False).encode("utf-8"),
    file_name="hospital_data_india.csv",
    mime="text/csv",
)

st.caption("Built with ❤️ using Streamlit, Pandas, and NumPy — for the Indian healthcare ecosystem 🇮🇳.")
