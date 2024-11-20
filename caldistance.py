import streamlit as st
import requests
import folium

# Function to retrieve the list of countries
def get_countries():
    base_url = "https://gcorea.gridweb.net/gcsetting/api/countries"
    headers = {
        'api-key': '0zFzEblgT7CJfLd0SuQTo11VtYEZT5GoTluVy1YXcQOs0H3XBl15kX61g802l9FCB4gCdYAFxbiU0yWl0MmC2bNKbigFZPc5jDHzMRbsgqHD9BnmpJgAYEGWkI1Y6v27QdhKMdN4EQbn1c5cXN1gvS7I40WPbewKTO6rE52Wk36kK2KtAKjEPTgqkfZrzJw30wuGi45p'
    }
    try:
        response = requests.get(base_url, headers=headers)
        if response.status_code == 200:
            return response.json()['data']  # Return the list of countries
        else:
            st.error(f"Error fetching countries: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error("An error occurred while retrieving countries.")
        st.write(str(e))
        return []

# Function to calculate distance and travel time
def calculate_distance(source_code, destination_code, source_country, destination_country):
    base_url = "https://gcorea.gridweb.net/external/api/calculate-distance"
    headers = {
        'api-key': '0zFzEblgT7CJfLd0SuQTo11VtYEZT5GoTluVy1YXcQOs0H3XBl15kX61g802l9FCB4gCdYAFxbiU0yWl0MmC2bNKbigFZPc5jDHzMRbsgqHD9BnmpJgAYEGWkI1Y6v27QdhKMdN4EQbn1c5cXN1gvS7I40WPbewKTO6rE52Wk36kK2KtAKjEPTgqkfZrzJw30wuGi45p'
    }
    payload = {
        "sourceGridCode": source_code,
        "destinationGridCode": destination_code,
        "sourceCountryCode": source_country,
        "destinationCountryCode": destination_country
    }
    try:
        response = requests.post(base_url, headers=headers, data=payload)
        if response.status_code == 200:
            return response.json()['data']  # Return distance and travel time data
        else:
            st.error(f"Error: {response.status_code}, Unable to calculate distance.")
            return None
    except requests.exceptions.RequestException as e:
        st.error("An error occurred while calculating distance.")
        st.write(str(e))
        return None

# Function to run the app
def run():
    # Streamlit App
    st.title("Travel Time and Distance Calculator")

    # Retrieve countries for dropdown
    countries = get_countries()
    if countries:
        country_dict = {country['country']: country['countryCode'] for country in countries}

        # Input for first grid code and country
        st.markdown("### **Enter Source Grid Code**")
        grid_code_1 = st.text_input("Source Grid Code", value="aaaa-ahgumc")
        country_name_1 = st.selectbox("Select Country for Source Grid Code", options=list(country_dict.keys()))
        country_code_1 = country_dict[country_name_1]

        # Input for second grid code and country
        st.markdown("### **Enter Destination Grid Code**")
        grid_code_2 = st.text_input("Destination Grid Code", value="aaaa-ahguhy")
        country_name_2 = st.selectbox("Select Country for Destination Grid Code", options=list(country_dict.keys()))
        country_code_2 = country_dict[country_name_2]

        # Button to calculate distance and travel time
        if st.button("Calculate Travel Time"):
            result = calculate_distance(grid_code_1, grid_code_2, country_code_1, country_code_2)

            if result:
                # Extract details
                source_address = result['sourceGridCode']['address']
                destination_address = result['destinationGridCode']['address']
                distance_km = result['distanceKm']
                travel_time = result['estimatedTravelTime']

                # Display results
                st.success("Distance and Travel Time Calculated Successfully!")
                st.markdown(f"### **Source Address**: \n{source_address}")
                st.markdown(f"### **Destination Address**: \n{destination_address}")
                st.markdown(f"### **Distance**: \n{distance_km} km")
                st.markdown(f"### **Estimated Travel Time**: \n{travel_time}")

                # Map visualization
                st.write("### Map Showing Travel Path")
                lat1, lon1 = float(result['sourceGridCode']['lat']), float(result['sourceGridCode']['lng'])
                lat2, lon2 = float(result['destinationGridCode']['lat']), float(result['destinationGridCode']['lng'])
                
                m = folium.Map(location=[(lat1 + lat2) / 2, (lon1 + lon2) / 2], zoom_start=14)
                folium.Marker([lat1, lon1], popup="Source").add_to(m)
                folium.Marker([lat2, lon2], popup="Destination").add_to(m)
                folium.PolyLine([[lat1, lon1], [lat2, lon2]], color="blue", weight=5).add_to(m)
                st.components.v1.html(m._repr_html_(), height=500)
    else:
        st.error("Failed to load countries. Please refresh the app.")
