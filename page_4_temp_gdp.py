import streamlit as st
import pandas as pd
import altair as alt

def show_page():
    st.title("4. Temp vs. GDP")
    st.info("Interactive visualization with country selection highlighting")
    
    # Try loading local file first
    try:
        df = pd.read_csv("group_data.csv")
    except FileNotFoundError:
        st.error("Error: 'group_data.csv' not found. Please ensure the file is in the correct directory.")
        st.stop()
    
    # GDP analysis preprocessing
    st.subheader("Temperature Patterns by GDP Tier")
    
    # Get max GDP per capita per country
    country_gdp_max = df.groupby('country', as_index=False)['GDP_per_capita_clean'].max()
    
    # Find the 10 countries with highest and lowest GDP
    high_gdp_countries = country_gdp_max.nlargest(10, 'GDP_per_capita_clean')['country']
    low_gdp_countries = country_gdp_max.nsmallest(10, 'GDP_per_capita_clean')['country']
    
    # Filter and prepare data
    filtered_data = df[df['country'].isin(high_gdp_countries.tolist() + low_gdp_countries.tolist())].copy()
    filtered_data['gdp_group'] = 'Other'
    filtered_data.loc[filtered_data['country'].isin(high_gdp_countries), 'gdp_group'] = 'High GDP'
    filtered_data.loc[filtered_data['country'].isin(low