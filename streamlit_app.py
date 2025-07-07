# streamlit_app.py (or app.py)
import streamlit as st
from PIL import Image
import os

# --- Import your page modules ---
# This line needs to match your actual file name (without the .py extension)
import page_1_ui_interaction # <--- THIS IS THE CRUCIAL LINE TO CHECK

# Also ensure your other page imports are correct if you've renamed them:
import page_2_within_visualization_interaction
import page_3_two_coordinated_visualizations


# ✅ Set page config FIRST (this must be at the top before anything renders)
st.set_page_config(
    page_title="Group 3 Term Project",
    page_icon="📊",
    layout="wide"
)

# --- Custom CSS for Background ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #FF0000; /* A true, vibrant red */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# --- Sidebar for Page Selection ---
st.sidebar.title("Project Pages")

# Use a dictionary to map user-friendly names to the functions that render each page.
pages = {
    "About Us": "about_us", # Handled directly in app.py
    "1. UI Interaction": page_1_ui_interaction.show_page, # <--- THIS LINE ALSO NEEDS TO BE CORRECT
    "2. Within Visualization Interaction": page_2_within_visualization_interaction.show_page,
    "3. Two Coordinated Visualizations": page_3_two_coordinated_visualizations.show_page,
}

# Create radio buttons in the sidebar
page_selection = st.sidebar.radio("Select a Page", list(pages.keys()), index=0)

# --- Display Page Content based on Selection ---
if page_selection == "About Us":
    # This is your original "About Us" page content, directly in app.py
    st.title("Group 3: Term Project Dashboard")
    st.write("Welcome to our application! This page provides information about our project.")

    st.markdown("### 🌱🌲🌳🥦 The Team")

    try:
        image = Image.open("allourpicscombined.png")
        st.image(image, width=500)
    except FileNotFoundError:
        st.error("Error: 'allourpicscombined.png' not found. Please ensure the image file is in the correct path.")

    st.markdown(
        """
        ### Our Mission:
        We aim to explore various aspects of data visualization and interaction within Streamlit.
        """
    )
    try:
        bc_logo = Image.open("BostonCollegeLynchLogo.png")
        st.image(bc_logo, width=250)
    except FileNotFoundError:
        st.error("Error: 'BostonCollegeLynchLogo.png' not found. Please ensure the image file is in the correct path.")

else:
    # Call the function associated with the selected page from the imported modules
    pages[page_selection]()

# --- Additional Sidebar Content ---
st.sidebar.markdown("---")
st.sidebar.write("This is our Streamlit Term Project Dashboard.")

# Display the Boston College Lynch Logo in the sidebar
try:
    bc_logo_path = os.path.join(os.path.dirname(__file__), "BostonCollegeLynchLogo.png")
    if os.path.exists(bc_logo_path):
        bc_logo = Image.open(bc_logo_path)
        st.sidebar.image(bc_logo, width=150)
    else:
        st.sidebar.warning(f"Warning: 'BostonCollegeLynchLogo.png' not found at {bc_logo_path}. Please check the path.")
except Exception as e:
    st.sidebar.error(f"An error occurred loading the logo: {e}")