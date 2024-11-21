import streamlit as st
import requests

# API Key
API_KEY = "0zFzEblgT7CJfLd0SuQTo11VtYEZT5GoTluVy1YXcQOs0H3XBl15kX61g802l9FCB4gCdYAFxbiU0yWl0MmC2bNKbigFZPc5jDHzMRbsgqHD9BnmpJgAYEGWkI1Y6v27QdhKMdN4EQbn1c5cXN1gvS7I40WPbewKTO6rE52Wk36kK2KtAKjEPTgqkfZrzJw30wuGi45p"
HEADERS = {"api-key": API_KEY, "Content-Type": "application/json"}

# URLs
GENERATE_URL = "https://gcorea.gridweb.net/gridcode/api/generate"
SAVE_URL = "https://gcorea.gridweb.net/gridcode/api/store"

def run():
    # App Title
    st.title("Grid Code Generator and Save!")

    # Input Fields for Latitude, Longitude, and Country Code
    lat = st.number_input("Enter Latitude", format="%.6f")
    lon = st.number_input("Enter Longitude", format="%.6f")
    country_code = st.text_input("Enter Country Code", placeholder="Enter the country code")

    # Button to Generate Grid Code
    if st.button("Generate GridCode"):
        # Prepare payload
        body = {
            "countryCode": country_code,
            "lat": lat,
            "long": lon
        }

        # Make API request
        response = requests.post(GENERATE_URL, headers=HEADERS, json=body)
        
        if response.status_code == 200:
            data = response.json()["data"]
            st.markdown(f"""
            <h2>Generated GridCode:</h2>
            <h1 style="color:blue; font-size:2.5em;">{data['gridcode']}</h1>
            <h3>Country: {data['country']}</h3>
            <h3>Address: {data['address']}</h3>
            """, unsafe_allow_html=True)
            
            # Save generated grid code in session state for later use
            st.session_state["grid_code"] = data
        else:
            st.error(f"Error: {response.json().get('message', 'Unknown error')}")

    # Section for Saving Grid Code
    if "grid_code" in st.session_state:
        st.header("Save Grid Code")
        generated_code = st.session_state["grid_code"]
        st.write(f"Generated Grid Code: **{generated_code['gridcode']}**")

        # Inputs for additional data
        category_id = st.text_input("Category ID", value="EA6955C1-153D-4AC8-AAD2-A37E29189920")
        title_description = st.text_input("Title/Description", value=generated_code['address'])
        name = st.text_input("Name (required)", placeholder="Enter a name for the Grid Code")
        lat_a = st.number_input("Lat A", value=lat, format="%.6f")
        long_a = st.number_input("Long A", value=lon, format="%.6f")
        lat_b = st.number_input("Lat B", value=lat + 0.000001, format="%.6f")
        long_b = st.number_input("Long B", value=lon + 0.000001, format="%.6f")
        lat_c = st.number_input("Lat C", value=lat + 0.000002, format="%.6f")
        long_c = st.number_input("Long C", value=lon + 0.000002, format="%.6f")

        # Add animated warning if 'name' is not filled
        if not name.strip():
            st.markdown(
                """
                <style>
                .blinking {
                    color: red;
                    animation: blinker 1.5s linear infinite;
                }
                @keyframes blinker {
                    50% { opacity: 0; }
                }
                </style>
                <p class="blinking">Remember to add a name before saving!</p>
                """, 
                unsafe_allow_html=True
            )

        if st.button("Save Grid Code"):
            # Validate required 'name' field
            if not name.strip():
                st.error("The 'Name' field is required to save the grid code.")
            else:
                save_body = {
                    "countryCode": country_code,
                    "gridcode": generated_code["gridcode"],
                    "categoryId": category_id,
                    "titleDescription": title_description,
                    "name": name,  # Include 'name' in the payload
                    "latA": lat_a,
                    "longA": long_a,
                    "latB": lat_b,
                    "longB": long_b,
                    "latC": lat_c,
                    "longC": long_c,
                    "generateAction": "NONE"
                }

                save_response = requests.post(SAVE_URL, headers=HEADERS, json=save_body)

                if save_response.status_code == 200:
                    st.success("Grid Code Saved Successfully!")
                    save_data = save_response.json()["data"]
                    
                    # Display only specific fields
                    st.markdown(f"""
                    <h3>Grid Code: {save_data['gridCode']}</h3>
                    <h3>Country Code: {save_data['countryCode']}</h3>
                    <h3>Details: {save_data['detail']}</h3>
                    """, unsafe_allow_html=True)
                elif save_response.status_code == 300:
                    st.warning("A grid code already exists at this location.")
                    data = save_response.json()["data"]
                    options = data.get("options", [])
                    choice = st.radio("Choose an action:", options)

                    if st.button("Confirm Action"):
                        save_body["generateAction"] = choice
                        confirm_response = requests.post(SAVE_URL, headers=HEADERS, json=save_body)
                        
                        if confirm_response.status_code == 200:
                            st.success(f"Action '{choice}' completed successfully!")
                            confirm_data = confirm_response.json()["data"]
                            # Display only specific fields after action
                            st.markdown(f"""
                            <h3>Grid Code: {confirm_data['gridCode']}</h3>
                            <h3>Country Code: {confirm_data['countryCode']}</h3>
                            <h3>Details: {confirm_data['detail']}</h3>
                            """, unsafe_allow_html=True)
                        else:
                            st.error(f"Error: {confirm_response.json().get('message', 'Unknown error')}")
                else:
                    st.error(f"Error: {save_response.json().get('message', 'Unknown error')}")
    else:
        st.info("Generate a grid code first to save it.")

if __name__ == "__main__":
    run()
