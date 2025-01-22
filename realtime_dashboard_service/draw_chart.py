import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go


# Function to split a dataframe into chunks for pagination
@st.cache_data(show_spinner=False)
def split_frame(input_df, rows):
    df = [input_df.loc[i: i + rows - 1, :] for i in range(0, len(input_df), rows)]
    return df


# Function to plot a colored bar chart for vote counts per candidate
def plot_colored_bar_chart(results):
    data_type = results['candidate_name']
    colors = plt.cm.viridis(np.linspace(0, 1, len(data_type)))
    plt.bar(data_type, results['total_votes'], color=colors)
    plt.xlabel('Candidate')
    plt.ylabel('Total Votes')
    plt.title('Vote Counts per Candidate')
    plt.xticks(rotation=90)
    return plt

# Function to plot a donut chart for vote distribution
def plot_donut_chart(data: pd.DataFrame, title='Donut Chart', type='candidate'):
    if type == 'candidate':
        labels = list(data['candidate_name'])
    elif type == 'gender':
        labels = list(data['gender'])

    sizes = list(data['total_votes'])
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')
    plt.title(title)
    return fig

# Function to plot a pie chart for vote distribution
def plot_pie_chart(data, title='Gender Distribution of Voters', labels=None):
    sizes = list(data.values())
    if labels is None:
        labels = list(data.keys())

    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    ax.axis('equal')
    plt.title(title)
    return fig

# Function to paginate a table
def paginate_table(table_data):
    top_menu = st.columns(3)
    with top_menu[0]:
        sort = st.radio("Sort Data", options=["Yes", "No"], horizontal=1, index=1)
    if sort == "Yes":
        with top_menu[1]:
            sort_field = st.selectbox("Sort By", options=table_data.columns)
        with top_menu[2]:
            sort_direction = st.radio(
                "Direction", options=["⬆️", "⬇️"], horizontal=True
            )
        table_data = table_data.sort_values(
            by=sort_field, ascending=sort_direction == "⬆️", ignore_index=True
        )
    pagination = st.container()

    bottom_menu = st.columns((4, 1, 1))
    with bottom_menu[2]:
        batch_size = st.selectbox("Page Size", options=[10, 25, 50, 100])
    with bottom_menu[1]:
        total_pages = (
            int(len(table_data) / batch_size) if int(len(table_data) / batch_size) > 0 else 1
        )
        current_page = st.number_input(
            "Page", min_value=1, max_value=total_pages, step=1
        )
    with bottom_menu[0]:
        st.markdown(f"Page **{current_page}** of **{total_pages}** ")

    pages = split_frame(table_data, batch_size)
    pagination.dataframe(data=pages[current_page - 1], use_container_width=True)


# Function to plot a US map with vote data
def plot_full_us_map(location_data):
    # Add coordinates to location_data
    location_data['latitude'] = location_data['state'].apply(lambda x: state_coordinates[x]['lat'])
    location_data['longitude'] = location_data['state'].apply(lambda x: state_coordinates[x]['lon'])
    location_data['state_code'] = location_data['state'].apply(lambda x: state_coordinates[x]['state code'])

    # Create the figure
    fig = go.Figure()

    # Add a choropleth layer for the state colors
    fig.add_trace(go.Choropleth(
        locationmode="USA-states",
        locations=location_data['state_code'],  # State abbreviations
        z=location_data['count'],   
        zmin=0,                           # Set minimum value for the color scale
        zmax=100,       # Data to color states
            colorscale=[
            [0, "blue"],  # Count <= 50 -> Blue
            [0.4, "blue"],
            [0.4, "red"], # Count > 50 -> Red
            [1, "red"]
        ],
        colorbar_title="Count"
    ))

    # Add state labels directly on the map
    fig.add_trace(go.Scattergeo(
        locationmode="USA-states",
        lat=location_data['latitude'],
        lon=location_data['longitude'],
        text=location_data.apply(lambda row: f"{row['state']}<br>votes: {row['count']}", axis=1),
        mode="text",
        textfont=dict(size=10, color="white"),
        showlegend=False
    ))

    # Update the map layout to focus on the US
    fig.update_layout(
        geo=dict(
            scope="usa",
            showland=True,
            landcolor="black",
        ),
        title="Custom US State Map with Counts"
    )

    return fig






















state_coordinates = {
    'Alabama': {'lat': 32.806671, 'lon': -86.791130 , 'state code': 'AL'},
    'Alaska': {'lat': 61.370716, 'lon': -152.404419, 'state code': 'AK'},
    'Arizona': {'lat': 33.729759, 'lon': -111.431221, 'state code': 'AZ'},
    'Arkansas': {'lat': 34.969704, 'lon': -92.373123, 'state code': 'AR'},
    'California': {'lat': 36.116203, 'lon': -119.681564,'state code': 'CA'},
    'Colorado': {'lat': 39.059811, 'lon': -105.311104, 'state code': 'CO'},
    'Connecticut': {'lat': 41.597782, 'lon': -72.755371, 'state code': 'CT'},
    'Delaware': {'lat': 39.318523, 'lon': -75.507141, 'state code': 'DE'},
    'Florida': {'lat': 27.766279, 'lon': -81.686783, 'state code': 'FL'},
    'Georgia': {'lat': 33.040619, 'lon': -83.643074, 'state code': 'GA'},
    'Hawaii': {'lat': 21.094318, 'lon': -157.498337, 'state code': 'HI'},
    'Idaho': {'lat': 44.240459, 'lon': -114.478828, 'state code': 'ID'},
    'Illinois': {'lat': 40.349457, 'lon': -88.986137, 'state code': 'IL'},
    'Indiana': {'lat': 39.849426, 'lon': -86.258278, 'state code': 'IN'},
    'Iowa': {'lat': 42.011539, 'lon': -93.210526, 'state code': 'IA'},
    'Kansas': {'lat': 38.526600, 'lon': -96.726486, 'state code': 'KS'},
    'Kentucky': {'lat': 37.668140, 'lon': -84.670067, 'state code': 'KY'},
    'Louisiana': {'lat': 31.169546, 'lon': -91.867805, 'state code': 'LA'},
    'Maine': {'lat': 44.693947, 'lon': -69.381927, 'state code': 'ME'},
    'Maryland': {'lat': 39.063946, 'lon': -76.802101, 'state code': 'MD'},
    'Massachusetts': {'lat': 42.230171, 'lon': -71.530106, 'state code': 'MA'},
    'Michigan': {'lat': 43.326618, 'lon': -84.536095, 'state code': 'MI'},
    'Minnesota': {'lat': 45.694454, 'lon': -93.900192, 'state code': 'MN'},
    'Mississippi': {'lat': 32.741646, 'lon': -89.678696, 'state code': 'MS'},
    'Missouri': {'lat': 38.456085, 'lon': -92.288368, 'state code': 'MO'},
    'Montana': {'lat': 46.921925, 'lon': -110.454353, 'state code': 'MT'},
    'Nebraska': {'lat': 41.125370, 'lon': -98.268082, 'state code': 'NE'},
    'Nevada': {'lat': 38.313515, 'lon': -117.055374, 'state code': 'NV'},
    'New Hampshire': {'lat': 43.452492, 'lon': -71.563896, 'state code': 'NH'},
    'New Jersey': {'lat': 40.298904, 'lon': -74.521011, 'state code': 'NJ'},
    'New Mexico': {'lat': 34.840515, 'lon': -106.248482, 'state code': 'NM'},
    'New York': {'lat': 42.165726, 'lon': -74.948051, 'state code': 'NY'},
    'North Carolina': {'lat': 35.630066, 'lon': -79.806419, 'state code': 'NC'},
    'North Dakota': {'lat': 47.528912, 'lon': -99.784012, 'state code': 'ND'},
    'Ohio': {'lat': 40.388783, 'lon': -82.764915, 'state code': 'OH'},
    'Oklahoma': {'lat': 35.565342, 'lon': -96.928917, 'state code': 'OK'},
    'Oregon': {'lat': 44.572021, 'lon': -122.070938, 'state code': 'OR'},
    'Pennsylvania': {'lat': 40.590752, 'lon': -77.209755, 'state code': 'PA'},
    'Rhode Island': {'lat': 41.680893, 'lon': -71.511780, 'state code': 'RI'},
    'South Carolina': {'lat': 33.856892, 'lon': -80.945007, 'state code': 'SC'},
    'South Dakota': {'lat': 44.299782, 'lon': -99.438828, 'state code': 'SD'},
    'Tennessee': {'lat': 35.747845, 'lon': -86.692345, 'state code': 'TN'},
    'Texas': {'lat': 31.054487, 'lon': -97.563461, 'state code': 'TX'},
    'Utah': {'lat': 40.150032, 'lon': -111.862434, 'state code': 'UT'},
    'Vermont': {'lat': 44.045876, 'lon': -72.710686, 'state code': 'VT'},
    'Virginia': {'lat': 37.769337, 'lon': -78.169968, 'state code': 'VA'},
    'Washington': {'lat': 47.400902, 'lon': -121.490494, 'state code': 'WA'},
    'West Virginia': {'lat': 38.491226, 'lon': -80.954456, 'state code': 'WV'},
    'Wisconsin': {'lat': 44.268543, 'lon': -89.616508, 'state code': 'WI'},
    'Wyoming': {'lat': 42.755966, 'lon': -107.302490, 'state code': 'WY'}
}