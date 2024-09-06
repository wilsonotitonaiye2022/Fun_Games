import streamlit as st
from streamlit_folium import folium_static
import folium
from folium import CustomIcon
import pandas as pd
import geopandas as gpd


# Load your dataframe
df = pd.read_csv("data/country_df.csv")

# Function to select countries based on Difficulty
def select_countries(df):
    easy = df[df['Difficulty'] == 'Easy'].sample(2)
    medium = df[df['Difficulty'] == 'Medium'].sample(2)
    hard = df[df['Difficulty'] == 'Hard'].sample(1)
    return pd.concat([easy, medium, hard])

# Function to create folium map
def create_map(selected_countries):
    # Create the base map
    m = folium.Map(location=[0, 0], zoom_start=1, tiles='cartodb positron')
    
    # Add the world map layer with black geometry
    folium.GeoJson(
        name='World Map',
        data=gpd.read_file("geo_files/countries.json"),
        style_function=lambda x: {'color': 'black'}
    ).add_to(m)
    
    # Convert selected countries to GeoDataFrame
    selected_countries_gdf = gpd.GeoDataFrame(
        selected_countries, 
        geometry=gpd.points_from_xy(selected_countries.Longitude, selected_countries.Latitude), 
        crs="EPSG:4326"
    )
    
    # Create a single FeatureGroup for all flags
    flags_layer = folium.FeatureGroup(name='Country Flags',show=False)
    
    # Add selected countries with green geometry and flag icons
    for _, row in selected_countries_gdf.iterrows():
        popup_html = f"""
        <b>{row['Country']}</b>
        <br><img src='{row['Flag']}' width='300px'><br>
        <b>Capital:</b> {row['Capital']}<br>
        <b>Continent:</b> {row['Continent']}<br>
        <b>Sub-Region:</b> {row['Sub-Region']}<br>
        <b>Currency:</b> {row['Currency']}<br>
        <b>2022 Population:</b> {row['2022 Population']}<br>
        <b>Area per Km sq:</b> {row['Area per Km sq']}<br>  
        <b>Density per Km sq:</b> {row['Density per Km sq']}<br>
        <b>Fun Fact:</b> <i>{row['Fun Facts']}</i><br>
        """

        icon = CustomIcon(
            icon_image=row['Flag'],
            icon_size=(30, 20),  # Adjust size to your needs
            icon_anchor=(15, 10)  # Adjust anchor to position the icon correctly
        )
        
        # Add markers to the flags_layer
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            icon=icon,
            popup=folium.Popup(popup_html, max_width=300)
        ).add_to(flags_layer)
    
    # Add the flags layer to the map
    flags_layer.add_to(m)
    
    # Add layer control
    folium.LayerControl(collapsed=False).add_to(m)
    
    return m


# Streamlit app
st.title(":world_map: Guess the Flag :earth_africa:")

st.markdown("### **Game Rules.**")
st.markdown("1. Click on the 'Generate 5 Random Flags' button to select 5 countries.")
st.markdown("2. Try to name the countries of the flags shown and mark location on flag.")
st.markdown("3. Click on the 'Show Answer' tab to see the countries and fun facts.")
st.markdown("4. At the top right corner on the map,  tick the Country Flags box to show flags on map.")
st.markdown("---")
st.markdown("### Have fun! :smile:")
st.markdown("---")


# Check if selected_countries is in session state
if 'selected_countries' not in st.session_state:
    st.session_state.selected_countries = select_countries(df)

if st.button("Generate 5 Random Flags"):
    st.session_state.selected_countries = select_countries(df)

    selected_countries = st.session_state.selected_countries
    st.markdown("---")

    tab1, tab2 = st.tabs(["**Guess The Map**", "**Show Answer**"])

    with tab1:
        st.markdown("#### Can you name the countries of the flags below :question:")
        st.write("---")

        # Group flags into pairs for the first two rows, and handle the last row separately.
        flags = [row['Flag'] for _, row in selected_countries.iterrows()]

        # Display the first two rows with 2 flags each.
        for i in range(0, 4, 2):  # Indices 0, 2
            cols = st.columns(2)  # Create two columns
            for j, col in enumerate(cols):
                if i + j < len(flags):  # Check if there is a flag to display
                    with col:
                        st.image(flags[i + j], width=100)
                        st.write("---")

        # Display the last row with only one flag.
        if len(flags) > 4:  # Check if there's a flag left for the third row
            cols = st.columns(2)
            with cols[0]:  # Place in the first column of the last row
                st.image(flags[4], width=100)
                st.write("---")

    with tab2:
        st.markdown("#### How did you do? :bulb:")
        st.write("---")

        # Extracting flag and country data from the DataFrame
        flags = [(row['Flag'], row['Country']) for _, row in selected_countries.iterrows()]

        # Display the first two rows with 2 flags each.
        for i in range(0, 4, 2):  # Indices 0, 2
            cols = st.columns(2)  # Create two columns
            for j, col in enumerate(cols):
                if i + j < len(flags):  # Check if there is a flag to display
                    with col:
                        st.image(flags[i + j][0], width=100)
                        st.write(f"**Country:** {flags[i + j][1]}")
                        st.write("---")

        # Display the last row with only one flag if available.
        if len(flags) > 4:  # Check if there's a flag left for the third row
            cols = st.columns(2)
            with cols[0]:  # Place in the first column of the last row
                st.image(flags[4][0], width=100)
                st.write(f"**Country:** {flags[4][1]}")
                st.write("---")

        # Create solution map
        st.markdown("#### Map of selected countries:")
        folium_static(create_map(selected_countries),width=800, height=700)

    st.sidebar.button("Reset", on_click=lambda: st.session_state.update(selected_countries=select_countries(df)))


