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

# Function to retrieve grid code details
def get_gridcode_details(grid_codes, country_codes):
    base_url = "https://gcorea.gridweb.net/external/api/search-gridcodes"
    api_key = "0zFzEblgT7CJfLd0SuQTo11VtYEZT5GoTluVy1YXcQOs0H3XBl15kX61g802l9FCB4gCdYAFxbiU0yWl0MmC2bNKbigFZPc5jDHzMRbsgqHD9BnmpJgAYEGWkI1Y6v27QdhKMdN4EQbn1c5cXN1gvS7I40WPbewKTO6rE52Wk36kK2KtAKjEPTgqkfZrzJw30wuGi45p"
    headers = {
        "api-key": api_key,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    payload = {f"gridCodes[{i}]": grid_codes[i] for i in range(len(grid_codes))}
    payload.update({f"countryCodes[{i}]": country_codes[i] for i in range(len(country_codes))})

    try:
        response = requests.post(base_url, headers=headers, data=payload)
        if response.status_code == 200:
            return response.json()['data']['details']
        else:
            st.error(f"Error: {response.status_code}. Unable to retrieve grid code details.")
            return []
    except requests.exceptions.RequestException as e:
        st.error("An error occurred while fetching grid code details.")
        st.write(str(e))
        return []

# Function to run the app
def run():
    # Streamlit App
    st.title("Navigation Between Two Grid Codes")

    # Retrieve countries for dropdown
    countries = get_countries()
    if countries:
        country_dict = {country['country']: country['countryCode'] for country in countries}

        # Input for first grid code and country
        st.markdown("### **Enter First Grid Code**")
        grid_code_1 = st.text_input("First Grid Code", value="aaaa-ahgumc")
        country_name_1 = st.selectbox("Select Country for First Grid Code", options=list(country_dict.keys()))
        country_code_1 = country_dict[country_name_1]

        # Input for second grid code and country
        st.markdown("### **Enter Second Grid Code**")
        grid_code_2 = st.text_input("Second Grid Code", value="aaaa-ahguhy")
        country_name_2 = st.selectbox("Select Country for Second Grid Code", options=list(country_dict.keys()))
        country_code_2 = country_dict[country_name_2]

        # Button to retrieve details and show map
        if st.button("Show Navigation"):
            details = get_gridcode_details([grid_code_1, grid_code_2], [country_code_1, country_code_2])

            if len(details) == 2:
                # Extract details
                lat1, lon1 = float(details[0]['lat']), float(details[0]['lng'])
                lat2, lon2 = float(details[1]['lat']), float(details[1]['lng'])
                address1, address2 = details[0]['address'], details[1]['address']

                # Create Folium map
                m = folium.Map(location=[(lat1 + lat2) / 2, (lon1 + lon2) / 2], zoom_start=15)

                # Add markers for the two locations
                folium.Marker([lat1, lon1], popup=f"GridCode 1: {grid_code_1}<br>Address: {address1}").add_to(m)
                folium.Marker([lat2, lon2], popup=f"GridCode 2: {grid_code_2}<br>Address: {address2}").add_to(m)

                # Add a PolyLine to connect the two points
                folium.PolyLine(locations=[[lat1, lon1], [lat2, lon2]], color="blue", weight=5).add_to(m)

                # Render map in Streamlit
                st.write("### Map with Navigation Path:")
                st.components.v1.html(m._repr_html_(), height=500)
            else:
                st.error("Failed to retrieve details for the provided grid codes. Please check the inputs.")
    else:
        st.error("Failed to load countries. Please refresh the app.")
