import streamlit as st
import pandas as pd
import altair as alt

def show_page():
    st.title("3. Pesticide Use vs. Crop Yield Analysis")
    st.info("Interactive visualization with country selection highlighting")
    
    # Try loading local file first
    try:
        df = pd.read_csv("group_data.csv")
    except FileNotFoundError:
        st.error("Error: 'group_data.csv' not found. Please ensure the file is in the correct directory.")
        st.stop()
    
    # Create the Altair visualization
    def create_chart(data):
        selection = alt.selection_point(
            fields=['country'], 
            empty='all',
            bind='legend',  # Makes legend interactive
            on='click'     # Makes points clickable
        )
        
        # Scatter plot with legend
        scatter = alt.Chart(data).mark_circle().encode(
            x=alt.X('pesticides_tonnes:Q', title='Pesticides (tonnes)'),
            y=alt.Y('hg/ha_yield:Q', title='Yield (hg/ha)'),
            color=alt.condition(
                selection, 
                alt.Color('country:N', legend=alt.Legend(title="Countries", columns=3)),
                alt.value('lightgray')),
            size=alt.Size('food_supply:Q', title='Food Supply'),
            tooltip=['country:N', 'pesticides_tonnes:Q', 'hg/ha_yield:Q', 'Item:N', 'food_supply:Q']
        ).add_params(
            selection
        ).properties(
            width=500,
            height=400
        ).interactive()
        
        # Box plot that responds to selection
        boxplot = alt.Chart(data).mark_boxplot().encode(
            x=alt.X('Item:N', title='Crop', axis=alt.Axis(labelAngle=-45)),
            y=alt.Y('pesticides_tonnes:Q', title='Pesticides (tonnes)'),
            color=alt.condition(
                selection,
                alt.Color('Item:N', legend=None),
                alt.value('lightgray'))
        ).transform_filter(
            selection
        ).properties(
            width=500,
            height=400
        )
        
        # Combine charts with title
        return (scatter | boxplot).properties(
            title='Interactive Exploration of Pesticide Use and Crop Yield'
        ).configure_view(
            strokeWidth=0
        ).configure_legend(
            labelFontSize=12,
            titleFontSize=13
        )
    
    # Display the chart with full width
    chart = create_chart(df)
    st.altair_chart(chart, use_container_width=True)
    
    # Optional: Add data table
    with st.expander("View Raw Data"):
        st.dataframe(df)

if __name__ == "__main__":
    show_page()