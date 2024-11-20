import streamlit as st
import folium
from folium.plugins import HeatMap
from streamlit_folium import folium_static
import pandas as pd
import json
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def run():
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
        "Delta": [5.8904, 5.6806], "Ebonyi": [6.3249, 8.1137], "Edo": [6.2024, 5.6218],
        "Ekiti": [7.6678, 5.2333], "Enugu": [6.4483, 7.5132], "Gombe": [10.2893, 11.1586],
        "Imo": [5.5149, 7.0793], "Jigawa": [11.6648, 9.5023], "Kaduna": [10.0269, 7.7420],
        "Kano": [11.6625, 8.3480], "Katsina": [12.9833, 7.6000], "Kebbi": [11.3182, 4.2034],
        "Kogi": [7.7799, 6.7143], "Kwara": [8.5943, 4.9519], "Lagos": [6.5244, 3.3792],
        "Nassarawa": [8.4671, 8.4791], "Niger": [9.6167, 5.0000], "Ogun": [7.2385, 3.4012],
        "Ondo": [7.2504, 5.2123], "Osun": [7.7848, 4.5724], "Oyo": [7.9919, 3.8689],
        "Plateau": [9.3075, 9.4625], "Rivers": [4.8152, 7.0491], "Sokoto": [12.9691, 5.2487],
        "Taraba": [8.3293, 10.3940], "Yobe": [12.9102, 11.9770], "Zamfara": [12.1583, 6.0095],
        "Federal Capital Territory": [9.0575, 7.4951]
    }
    
    # Create a Folium map centered on Nigeria
    m = folium.Map(location=[9.0820, 8.6753], zoom_start=6)

    # Add choropleth layer for hospital distribution
    folium.Choropleth(
        geo_data=state_geo,
        name="Hospitals",
        data=df_hospitals,
        columns=["State", "Total_Hospitals"],
        key_on="feature.properties.name",  # Match state name in GeoJSON
        fill_color="YlGnBu",
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name="Total Number of Hospitals"
    ).add_to(m)

    # Add markers with popups for hospital data
    for state, row in df_hospitals.iterrows():
        folium.Marker(
            location=state_coords[state],
            popup=f"State: {state}<br>Primary: {row['Primary']}<br>Secondary: {row['Secondary']}<br>Tertiary: {row['Tertiary']}<br>Total Hospitals: {row['Total_Hospitals']}"
        ).add_to(m)

    # Add pie charts for hospital ownership
    for state, row in df_ownership.iterrows():
        # Generate pie chart for each state
        fig, ax = plt.subplots()
        ax.pie([row["Public"], row["Private"]], labels=["Public", "Private"], autopct='%1.1f%%', startangle=90)
        ax.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
        pie_chart = BytesIO()
        plt.savefig(pie_chart, format="png")
        pie_chart.seek(0)
        encoded_img = base64.b64encode(pie_chart.getvalue()).decode("utf-8")
        folium.Marker(
            location=state_coords[state],
            popup=f"<img src='data:image/png;base64,{encoded_img}' />"
        ).add_to(m)

    # Display the map
    folium_static(m)

# Run the app
if __name__ == "__main__":
    run()
