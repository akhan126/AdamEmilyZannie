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
    filtered_data.loc[filtered_data['country'].isin(low_gdp_countries), 'gdp_group'] = 'Low GDP'
    filtered_data = filtered_data[filtered_data['gdp_group'].isin(['High GDP', 'Low GDP'])]
    
    # Create interactive selection
    selection = alt.selection_point(
        fields=['country'],
        empty=True,
        bind='legend',
        on='click'
    )
    
    # Create the visualizations
    def create_dashboard(data):
        # Temperature density plot
        density = alt.Chart(data).transform_density(
            'avg_temp',
            groupby=['gdp_group'],
            as_=['avg_temp', 'density'],
            extent=[data['avg_temp'].min(), data['avg_temp'].max()],
            bandwidth=1
        ).mark_area(opacity=0.3).encode(
            x=alt.X('avg_temp:Q', title='Average Temperature (°C)'),
            y=alt.Y('density:Q', title='Density'),
            color=alt.Color('gdp_group:N', legend=alt.Legend(title="GDP Group", orient='bottom'))
        ).properties(height=200)
        
        # Scatter plot
        scatter = alt.Chart(data).mark_circle(size=80).encode(
            x=alt.X('GDP_per_capita_clean:Q', 
                   title='GDP per Capita (log scale)',
                   scale=alt.Scale(type='log')),
            y=alt.Y('avg_temp:Q', title='Average Temperature (°C)'),
            color=alt.condition(
                selection,
                alt.Color('gdp_group:N', legend=None),
                alt.value('lightgray')
            ),
            size=alt.condition(selection, alt.value(150), alt.value(80)),
            tooltip=['country:N', 'GDP_per_capita_clean:Q', 'avg_temp:Q', 'gdp_group:N']
        ).add_params(
            selection
        ).properties(height=300)
        
        # Country distribution plot
        country_dist = alt.Chart(data).mark_boxplot().encode(
            x=alt.X('avg_temp:Q', title='Temperature Distribution'),
            y=alt.Y('country:N', title='', 
                   sort=alt.EncodingSortField('GDP_per_capita_clean', order='descending')),
            color=alt.condition(
                selection,
                alt.Color('gdp_group:N', legend=None),
                alt.value('lightgray')
            )
        ).transform_filter(
            selection
        ).properties(height=400)
        
        # Combine charts
        return alt.vconcat(
            density,
            scatter,
            country_dist
        ).properties(
            title=alt.TitleParams(
                'Comparing Temperature Patterns Across GDP Tiers',
                subtitle=['Click on points or legend to explore relationships'],
                anchor='middle'
            )
        ).configure_view(
            strokeWidth=0
        ).configure_axis(
            labelFontSize=12,
            titleFontSize=14
        )
    
    # Create and display the dashboard
    dashboard = create_dashboard(filtered_data)
    st.altair_chart(dashboard, use_container_width=True)
    
    # Data summary
    with st.expander("ℹ️ About This Visualization"):
        st.markdown("""
        - **Top Chart**: Shows temperature distribution density for high vs low GDP countries
        - **Middle Chart**: Scatter plot of GDP vs temperature (log scale)
        - **Bottom Chart**: Temperature distributions for individual countries
        - **Interactivity**: Click on points or legend items to highlight across all charts
        """)
        
        st.write("Countries analyzed:")
        col1, col2 = st.columns(2)
        with col1:
            st.write("**High GDP Countries:**")
            st.write(high_gdp_countries.tolist())
        with col2:
            st.write("**Low GDP Countries:**")
            st.write(low_gdp_countries.tolist())

if __name__ == "__main__":
    show_page()