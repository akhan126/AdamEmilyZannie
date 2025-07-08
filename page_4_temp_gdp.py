import streamlit as st
import pandas as pd
import altair as alt

def show_page():
    st.title("4. Temp vs. GDP")
    st.info("Interactive visualization with country selection highlighting")
    
        try:
        df = pd.read_csv("group_data.csv")
    except FileNotFoundError:
        st.error("Error: 'group_data.csv' not found. Please ensure the file is in the correct directory.")
        st.stop()