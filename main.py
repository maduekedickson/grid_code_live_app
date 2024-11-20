import streamlit as st
import importlib

# Function to load the selected app dynamically
def load_app(app_name):
    try:
        # Import the app dynamically based on the selection
        app_module = importlib.import_module(app_name)  # Import the selected app
        app_module.run()  # Assuming each app has a run() function
    except ModuleNotFoundError:
        st.error(f"App {app_name} not found!")

# Sidebar for app selection using radio buttons
st.sidebar.title("App Selector")
app_option = st.sidebar.radio("Choose App", ["Home","Nigeria Hospital Map", "Generate Grid Code", "Validate Grid Code", "View Code On Map", "Navigation", "Distance Calculator"])

# Conditional loading based on radio button selection
if app_option == "Home":
    load_app("home")  # Import and run generate.py
elif app_option == "Nigeria Hospital Map":
    load_app("map")  # Import and run validate.py
elif app_option == "Generate Grid Code":
    load_app("generate")  # Import and run validate.py    
elif app_option == "Validate Grid Code":
    load_app("validate")  # Import and run spot.py
elif app_option == "View Code On Map":
    load_app("spot")  # Import and run navigate.py
elif app_option == "Navigation":
    load_app("navigate")  # Import and run caldistance.py
elif app_option == "Distance Calculator":
    load_app("caldistance")  # Import and run map.py
