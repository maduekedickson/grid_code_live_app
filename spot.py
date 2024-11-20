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

# Function to run the app
def run():
    # Streamlit app
    st.title("Grid Code Verification with Map")

    # Retrieve countries and create a dropdown
    countries = get_countries()
    if countries:
        country_dict = {country['country']: country['countryCode'] for country in countries}
        country_name = st.selectbox("Select a Country:", options=list(country_dict.keys()))
        country_code = country_dict[country_name]
    else:
        country_name = ""
        country_code = ""

    # Input for grid code
    st.markdown("### **Enter Grid Code**")
    grid_code = st.text_input("", value="aaaa-ahgumc", help="Enter the grid code you want to verify.")
    st.markdown(f"<style>input {{font-size: 18px; font-weight: bold;}}</style>", unsafe_allow_html=True)

    # Button to trigger verification
    if st.button("Verify"):
        base_url = "https://gcorea.gridweb.net/external/api/verify-gridcode"
        params = {
            'gridCode': grid_code,
            'countryCode': country_code
        }
        headers = {
            'api-key': '0zFzEblgT7CJfLd0SuQTo11VtYEZT5GoTluVy1YXcQOs0H3XBl15kX61g802l9FCB4gCdYAFxbiU0yWl0MmC2bNKbigFZPc5jDHzMRbsgqHD9BnmpJgAYEGWkI1Y6v27QdhKMdN4EQbn1c5cXN1gvS7I40WPbewKTO6rE52Wk36kK2KtAKjEPTgqkfZrzJw30wuGi45p'
        }

        try:
            response = requests.get(base_url, headers=headers, params=params)
            if response.status_code == 200:
                result = response.json()
                data = result.get("data", {})
                if data.get("isValid"):
                    st.success(f"The grid code **'{grid_code}'** is valid for country **'{country_name}'**.")

                    # Get coordinates for the map
                    lat = data.get("latitude", 25.226105)  # Example: use real latitude if available
                    lon = data.get("longitude", 55.283578)  # Example: use real longitude if available

                    # Create a Folium map
                    m = folium.Map(location=[lat, lon], zoom_start=14)
                    folium.Marker([lat, lon], popup="GridCode Location").add_to(m)

                    # Render the map in Streamlit
                    st.write("### Map showing GridCode Location:")
                    st.components.v1.html(m._repr_html_(), height=500)

                else:
                    st.error(f"The grid code **'{grid_code}'** is invalid for country **'{country_name}'**.")
            else:
                st.error(f"Error: {response.status_code}. Unable to verify the grid code.")
        except requests.exceptions.RequestException as e:
            st.error("An error occurred. Please try again later.")
            st.write(str(e))
