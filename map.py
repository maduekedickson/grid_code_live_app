import streamlit as st 
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import pandas as pd
import json
import matplotlib.pyplot as plt
from io import BytesIO
import base64

# Load GeoJSON file for Nigeria state boundaries
geojson_file = "ng.json"  # Ensure this file exists in the same directory
with open(geojson_file, "r") as f:
    state_geo = json.load(f)

# Hospital data dictionary
hospital_data = {
    'Abia': {'Primary': 938, 'Secondary': 245, 'Tertiary': 7, 'Total': 1190},
    'Adamawa': {'Primary': 862, 'Secondary': 43, 'Tertiary': 1, 'Total': 906},
    'Akwa Ibom': {'Primary': 535, 'Secondary': 208, 'Tertiary': 1, 'Total': 743},
    'Anambra': {'Primary': 728, 'Secondary': 436, 'Tertiary': 3, 'Total': 1167},
    'Bauchi': {'Primary': 1188, 'Secondary': 61, 'Tertiary': 6, 'Total': 1255},
    'Bayelsa': {'Primary': 225, 'Secondary': 74, 'Tertiary': 4, 'Total': 303},
    'Benue': {'Primary': 1489, 'Secondary': 121, 'Tertiary': 3, 'Total': 1613},
    'Borno': {'Primary': 370, 'Secondary': 55, 'Tertiary': 2, 'Total': 427},
    'Cross River': {'Primary': 1035, 'Secondary': 137, 'Tertiary': 3, 'Total': 1175},
    'Delta': {'Primary': 648, 'Secondary': 171, 'Tertiary': 2, 'Total': 821},
    'Ebonyi': {'Primary': 657, 'Secondary': 59, 'Tertiary': 3, 'Total': 719},
    'Edo': {'Primary': 927, 'Secondary': 294, 'Tertiary': 11, 'Total': 1232},
    'Ekiti': {'Primary': 431, 'Secondary': 101, 'Tertiary': 3, 'Total': 535},
    'Enugu': {'Primary': 678, 'Secondary': 353, 'Tertiary': 6, 'Total': 1037},
    'Gombe': {'Primary': 637, 'Secondary': 51, 'Tertiary': 1, 'Total': 689},
    'Imo': {'Primary': 822, 'Secondary': 373, 'Tertiary': 2, 'Total': 1197},
    'Jigawa': {'Primary': 775, 'Secondary': 34, 'Tertiary': 1, 'Total': 810},
    'Kaduna': {'Primary': 1276, 'Secondary': 124, 'Tertiary': 20, 'Total': 1420},
    'Kano': {'Primary': 1344, 'Secondary': 136, 'Tertiary': 6, 'Total': 1486},
    'Katsina': {'Primary': 1902, 'Secondary': 40, 'Tertiary': 3, 'Total': 1945},
    'Kebbi': {'Primary': 887, 'Secondary': 60, 'Tertiary': 2, 'Total': 949},
    'Kogi': {'Primary': 1081, 'Secondary': 153, 'Tertiary': 4, 'Total': 1238},
    'Kwara': {'Primary': 782, 'Secondary': 209, 'Tertiary': 3, 'Total': 994},
    'Lagos': {'Primary': 1475, 'Secondary': 714, 'Tertiary': 7, 'Total': 2196},
    'Nassarawa': {'Primary': 999, 'Secondary': 47, 'Tertiary': 2, 'Total': 1048},
    'Niger': {'Primary': 1498, 'Secondary': 64, 'Tertiary': 3, 'Total': 1565},
    'Ogun': {'Primary': 1000, 'Secondary': 205, 'Tertiary': 2, 'Total': 1207},
    'Ondo': {'Primary': 722, 'Secondary': 98, 'Tertiary': 4, 'Total': 824},
    'Osun': {'Primary': 1010, 'Secondary': 55, 'Tertiary': 6, 'Total': 1071},
    'Oyo': {'Primary': 900, 'Secondary': 568, 'Tertiary': 10, 'Total': 1478},
    'Plateau': {'Primary': 1248, 'Secondary': 94, 'Tertiary': 3, 'Total': 1345},
    'Rivers': {'Primary': 460, 'Secondary': 120, 'Tertiary': 6, 'Total': 586},
    'Sokoto': {'Primary': 797, 'Secondary': 37, 'Tertiary': 3, 'Total': 837},
    'Taraba': {'Primary': 903, 'Secondary': 40, 'Tertiary': 1, 'Total': 944},
    'Yobe': {'Primary': 488, 'Secondary': 30, 'Tertiary': 2, 'Total': 520},
    'Zamfara': {'Primary': 708, 'Secondary': 36, 'Tertiary': 3, 'Total': 747},
    'Federal Capital Territory': {'Primary': 487, 'Secondary': 101, 'Tertiary': 8, 'Total': 596}
}

# Ownership data
ownership_data = {
    "State": ["Abia", "Adamawa", "Akwa Ibom", "Anambra", "Bauchi", "Bayelsa", "Benue", "Borno",
              "Cross River", "Delta", "Ebonyi", "Edo", "Ekiti", "Enugu", "Gombe", "Imo",
              "Jigawa", "Kaduna", "Kano", "Katsina", "Kebbi", "Kogi", "Kwara", "Lagos",
              "Nassarawa", "Niger", "Ogun", "Ondo", "Osun", "Oyo", "Plateau", "Rivers",
              "Sokoto", "Taraba", "Yobe", "Zamfara", "Federal Capital Territory"],
    "Public": [760, 817, 545, 658, 1144, 259, 1126, 380, 1062, 550, 534, 646, 380, 612, 
               627, 683, 794, 1099, 1274, 1867, 916, 1005, 661, 415, 828, 1368, 642, 
               661, 874, 845, 997, 457, 802, 803, 503, 717, 317],
    "Private": [430, 89, 198, 509, 111, 44, 487, 47, 113, 271, 185, 586, 155, 425,
                62, 514, 16, 321, 212, 78, 33, 233, 333, 1781, 220, 197, 565, 
                163, 197, 633, 348, 129, 35, 141, 17, 30, 279]
}

# Convert hospital and ownership data to DataFrames
df_hospitals = pd.DataFrame([
    {'State': state, 'Primary': data['Primary'], 'Secondary': data['Secondary'], 
     'Tertiary': data['Tertiary'], 'Total_Hospitals': data['Total']}
    for state, data in hospital_data.items()
])

df_ownership = pd.DataFrame(ownership_data)

# State coordinates
state_coords = {
    "Abia": [5.4527, 7.5248], "Adamawa": [9.3265, 12.3984], "Akwa Ibom": [5.0527, 7.9337],
    "Anambra": [6.2209, 7.0670], "Bauchi": [10.3113, 9.8432], "Bayelsa": [4.7719, 6.0699],
    "Benue": [7.3369, 8.7400], "Borno": [11.8333, 13.1500], "Cross River": [5.9631, 8.3333],
    "Delta": [5.8904, 5.6806], "Ebonyi": [6.3249, 8.1137], "Edo": [6.3405, 5.6200],
    "Ekiti": [7.6214, 5.2195], "Enugu": [6.5244, 7.5186], "Gombe": [10.2993, 11.1750],
    "Imo": [5.5720, 7.0588], "Jigawa": [12.1544, 9.9462], "Kaduna": [10.5105, 7.4165],
    "Kano": [12.0022, 8.5919], "Katsina": [12.9900, 7.6000], "Kebbi": [12.4554, 4.1970],
    "Kogi": [7.7335, 6.6906], "Kwara": [8.4799, 4.5418], "Lagos": [6.5244, 3.3792],
    "Nassarawa": [8.5400, 7.7100], "Niger": [9.9304, 5.5983], "Ogun": [7.1603, 3.3568],
    "Ondo": [7.2507, 5.2103], "Osun": [7.5629, 4.5196], "Oyo": [7.3775, 3.9470],
    "Plateau": [9.8965, 8.8583], "Rivers": [4.7856, 6.9086], "Sokoto": [13.0532, 5.2347],
    "Taraba": [8.8937, 11.3785], "Yobe": [12.0000, 11.5000], "Zamfara": [12.1702, 6.6621],
    "Federal Capital Territory": [9.0765, 7.3986]
}

# Function to generate pie charts for ownership
def generate_pie_chart(public, private, state_name):
    fig, ax = plt.subplots(figsize=(2, 2))  # Smaller chart size
    ax.pie([public, private], labels=['Public', 'Private'], autopct='%1.1f%%', colors=['blue', 'orange'])
    ax.set_title(f'Ownership in {state_name}', fontsize=8)  # Small font size for title

    # Save the chart to a bytes buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png', bbox_inches='tight', dpi=80)  # Adjust for tighter layout
    buffer.seek(0)
    image_base64 = base64.b64encode(buffer.read()).decode('utf-8')
    buffer.close()
    plt.close(fig)

    # Return the image as an HTML image element
    return f'<img src="data:image/png;base64,{image_base64}" width="150" height="150"/>'

# Streamlit app
st.title("Nigeria Hospital Data Visualization")
st.write("This application visualizes healthcare facilities and ownership across Nigerian states using Folium.")

# Create the base map
map_center = [9.0820, 8.6753]  # Center of Nigeria
hospital_map = folium.Map(location=map_center, zoom_start=6, tiles='cartodbpositron', width='100%', height='100%')

# Add a choropleth layer for total hospitals
folium.Choropleth(
    geo_data=state_geo,
    name='Hospital',
    data=df_hospitals,
    columns=['State', 'Total_Hospitals'],
    key_on='feature.properties.name',  # Match GeoJSON's 'name' property
    fill_color='YlGn',  # Yellow to Green color scale
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Total Hospitals per State',
    nan_fill_color='white'  # Fill missing data with white
).add_to(hospital_map)

# Add pop-up markers with charts for hospital types
for _, row in df_hospitals.iterrows():
    state = row['State']
    primary = row['Primary']
    secondary = row['Secondary']
    tertiary = row['Tertiary']
    
    # Generate chart HTML
    chart_html = f"""
    <h4>{state} Hospital Distribution</h4>
    <ul>
        <li><b>Primary:</b> {primary}</li>
        <li><b>Secondary:</b> {secondary}</li>
        <li><b>Tertiary:</b> {tertiary}</li>
    </ul>
    """
    iframe = folium.IFrame(html=chart_html, width=230, height=180)  # Smaller frame
    popup = folium.Popup(iframe, max_width=330)
    
    # Add a marker for each state
    folium.Marker(
        location=state_coords[state],
        popup=popup,
        tooltip='View Chart',  # Tooltip that says "View Chart"
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(hospital_map)

# Create a separate layer for ownership
ownership_layer = folium.FeatureGroup(name='Ownership').add_to(hospital_map)

# Add pop-up markers with pie charts for ownership
for _, row in df_ownership.iterrows():
    state = row['State']
    public = row['Public']
    private = row['Private']
    pie_chart_html = generate_pie_chart(public, private, state)
    iframe = folium.IFrame(html=pie_chart_html, width=200, height=150)  # Smaller frame
    popup = folium.Popup(iframe, max_width=300)
    
    # Add a marker for each state in the ownership layer
    folium.Marker(
        location=state_coords[state],
        popup=popup,
        tooltip='Click me',  # Tooltip that says "Click me"
        icon=folium.Icon(color='green', icon='ok-sign')  # Different color for ownership markers
    ).add_to(ownership_layer)

# Data for special hospitals (Federal Medical Centres)
hospital_data = {
    "Federal Medical Centre, Abeokuta": {"State": "Ogun", "Latitude": 7.143419327, "Longitude": 3.378607282},
    "Federal Medical Centre, Asaba": {"State": "Delta", "Latitude": 6.212104318, "Longitude": 6.713036944},
    "Federal Medical Centre, Azare": {"State": "Bauchi", "Latitude": 11.67533741, "Longitude": 10.19812159},
    "Federal Medical Centre, Bida": {"State": "Niger", "Latitude": 9.074048756, "Longitude": 5.999023284},
    "Federal Medical Centre, Birnin Kebbi": {"State": "Kebbi", "Latitude": 12.53124374, "Longitude": 4.398133239},
    "Federal Medical Centre, Birnin Kudu": {"State": "Jigawa", "Latitude": 11.4424984, "Longitude": 9.486040674},
    "Federal Medical Centre, Ebutte-Metta": {"State": "Lagos", "Latitude": 6.484509599, "Longitude": 3.380932595},
    "Federal Medical Centre, Gombe": {"State": "Gombe", "Latitude": 10.54642781, "Longitude": 11.66556592},
    "Federal Medical Centre, Gusau": {"State": "Zamfara", "Latitude": 12.18402014, "Longitude": 6.687640206},
    "Federal Medical Centre, Ido-Ekiti": {"State": "Ekiti", "Latitude": 7.84505362, "Longitude": 5.191756613},
    "Federal Medical Centre, Jalingo": {"State": "Taraba", "Latitude": 8.893031549, "Longitude": 11.37792367},
    "Federal Medical Centre, Katsina": {"State": "Katsina", "Latitude": 12.98874259, "Longitude": 7.578795667},
    "Federal Medical Centre, Keffi": {"State": "Nassarawa", "Latitude": 8.84591301, "Longitude": 7.886092023},
    "Federal Medical Centre, Lokoja": {"State": "Kogi", "Latitude": 7.800029332, "Longitude": 6.742407805},
    "Federal Medical Centre, Makurdi": {"State": "Benue", "Latitude": 7.729695594, "Longitude": 8.519789544},
    "Federal Medical Centre, Nguru": {"State": "Yobe", "Latitude": 13.09442664, "Longitude": 10.85049674},
    "Federal Medical Centre, Owerri": {"State": "Imo", "Latitude": 5.504379836, "Longitude": 7.027241334},
    "Federal Medical Centre, Owo": {"State": "Ondo", "Latitude": 7.21387871, "Longitude": 5.599709236},
    "Federal Medical Centre, Umuahia": {"State": "Abia", "Latitude": 5.522611222, "Longitude": 7.493418789},
    "Federal Medical Centre, Yenogoa": {"State": "Bayelsa", "Latitude": 4.937312778, "Longitude": 6.266654144},
    "Federal Medical Centre, Yola": {"State": "Adamawa", "Latitude": 9.209628149, "Longitude": 12.47921274},
    "Federal Staff Hospital, Jabi": {"State": "Abuja", "Latitude": 9.020383121, "Longitude": 7.498974734},
}

# Convert hospital data into a DataFrame
df_fmc = pd.DataFrame([
    {"Hospital": name, "State": details["State"], "Latitude": details["Latitude"], "Longitude": details["Longitude"]}
    for name, details in hospital_data.items()
])

# Add a new layer for Federal Medical Centres
fmc_layer = folium.FeatureGroup(name='Federal Medical Centres').add_to(hospital_map)

# Add markers for Federal Medical Centres
for _, row in df_fmc.iterrows():
    state = row['State']
    hospital_name = row['Hospital']
    
    # Popup content for hospital information
    popup_content = f"<strong>{hospital_name}</strong><br>State: {state}"
    folium.Marker(
        location=[row['Latitude'], row['Longitude']],
        popup=popup_content,
        tooltip='Click me',  # Tooltip for each hospital marker
        icon=folium.Icon(color='red', icon='plus-sign')  # Red icon for hospitals
    ).add_to(fmc_layer)

# Add state labels with bold text
for state, coords in state_coords.items():
    folium.Marker(
        location=coords,
        icon=folium.DivIcon(html=f'<div style="font-size: 9pt; font-weight: bold">{state}</div>')
    ).add_to(hospital_map)

# Add LayerControl to toggle between layers
folium.LayerControl().add_to(hospital_map)

# Render map
folium_static(hospital_map)
