import streamlit as st
import pandas as pd
import altair as alt

def show_page():
    st.title("2. Pesticide Use vs. Crop Yield Analysis")
    st.info("Interactive visualization with country selection highlighting")
    
    # Try loading local file first
    try:
        df = pd.read_csv("group_data.csv")
    except FileNotFoundError:
        st.error("Error: 'group_data.csv' not found. Please ensure the file is in the correct directory.")
        st.stop()
    
    # Create the Altair visualization
    def create_chart(data):
        selection = alt.selection_point(fields=['country'], empty='all')
        
        scatter = alt.Chart(data).mark_circle().encode(
            x=alt.X('pesticides_tonnes:Q', title='Pesticides (tonnes)'),
            y=alt.Y('hg/ha_yield:Q', title='Yield (hg/ha)'),
            color=alt.condition(selection, 
                             alt.Color('country:N', legend=None),
                             alt.value('lightgray')),
            size=alt.Size('food_supply:Q', title='Food Supply'),
            tooltip=['country:N', 'pesticides_tonnes:Q', 'hg/ha_yield:Q', 'Item:N']
        ).add_params(
            selection
        ).properties(
            width=500,
            height=400
        )
        
        boxplot = alt.Chart(data).mark_boxplot().encode(
            x=alt.X('Item:N', title='Crop'),
            y=alt.Y('pesticides_tonnes:Q', title='Pesticides (tonnes)'),
            color=alt.condition(selection,
                              alt.Color('Item:N', legend=None),
                              alt.value('lightgray'))
        ).transform_filter(
            selection
        ).properties(
            width=500,
            height=400
        )
        
        return (scatter | boxplot).properties(
            title='Interactive Exploration of Pesticide Use and Crop Yield'
        ).configure_axis(
            labelAngle=-45
        )
    
    # Display the chart
    chart = create_chart(df)
    st.altair_chart(chart, use_container_width=True)
    
    # Optional: Add data table
    with st.expander("View Raw Data"):
        st.dataframe(df)