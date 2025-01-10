import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import simplejson as json
import streamlit as st
from kafka import KafkaConsumer
from streamlit_autorefresh import st_autorefresh
import psycopg2
import plotly.express as px
import plotly.graph_objects as go

state_coordinates = {
    'Alabama': {'lat': 32.806671, 'lon': -86.791130},
    'Alaska': {'lat': 61.370716, 'lon': -152.404419},
    'Arizona': {'lat': 33.729759, 'lon': -111.431221},
    'Arkansas': {'lat': 34.969704, 'lon': -92.373123},
    'California': {'lat': 36.116203, 'lon': -119.681564},
    'Colorado': {'lat': 39.059811, 'lon': -105.311104},
    'Connecticut': {'lat': 41.597782, 'lon': -72.755371},
    'Delaware': {'lat': 39.318523, 'lon': -75.507141},
    'Florida': {'lat': 27.766279, 'lon': -81.686783},
    'Georgia': {'lat': 33.040619, 'lon': -83.643074},
    'Hawaii': {'lat': 21.094318, 'lon': -157.498337},
    'Idaho': {'lat': 44.240459, 'lon': -114.478828},
    'Illinois': {'lat': 40.349457, 'lon': -88.986137},
    'Indiana': {'lat': 39.849426, 'lon': -86.258278},
    'Iowa': {'lat': 42.011539, 'lon': -93.210526},
    'Kansas': {'lat': 38.526600, 'lon': -96.726486},
    'Kentucky': {'lat': 37.668140, 'lon': -84.670067},
    'Louisiana': {'lat': 31.169546, 'lon': -91.867805},
    'Maine': {'lat': 44.693947, 'lon': -69.381927},
    'Maryland': {'lat': 39.063946, 'lon': -76.802101},
    'Massachusetts': {'lat': 42.230171, 'lon': -71.530106},
    'Michigan': {'lat': 43.326618, 'lon': -84.536095},
    'Minnesota': {'lat': 45.694454, 'lon': -93.900192},
    'Mississippi': {'lat': 32.741646, 'lon': -89.678696},
    'Missouri': {'lat': 38.456085, 'lon': -92.288368},
    'Montana': {'lat': 46.921925, 'lon': -110.454353},
    'Nebraska': {'lat': 41.125370, 'lon': -98.268082},
    'Nevada': {'lat': 38.313515, 'lon': -117.055374},
    'New Hampshire': {'lat': 43.452492, 'lon': -71.563896},
    'New Jersey': {'lat': 40.298904, 'lon': -74.521011},
    'New Mexico': {'lat': 34.840515, 'lon': -106.248482},
    'New York': {'lat': 42.165726, 'lon': -74.948051},
    'North Carolina': {'lat': 35.630066, 'lon': -79.806419},
    'North Dakota': {'lat': 47.528912, 'lon': -99.784012},
    'Ohio': {'lat': 40.388783, 'lon': -82.764915},
    'Oklahoma': {'lat': 35.565342, 'lon': -96.928917},
    'Oregon': {'lat': 44.572021, 'lon': -122.070938},
    'Pennsylvania': {'lat': 40.590752, 'lon': -77.209755},
    'Rhode Island': {'lat': 41.680893, 'lon': -71.511780},
    'South Carolina': {'lat': 33.856892, 'lon': -80.945007},
    'South Dakota': {'lat': 44.299782, 'lon': -99.438828},
    'Tennessee': {'lat': 35.747845, 'lon': -86.692345},
    'Texas': {'lat': 31.054487, 'lon': -97.563461},
    'Utah': {'lat': 40.150032, 'lon': -111.862434},
    'Vermont': {'lat': 44.045876, 'lon': -72.710686},
    'Virginia': {'lat': 37.769337, 'lon': -78.169968},
    'Washington': {'lat': 47.400902, 'lon': -121.490494},
    'West Virginia': {'lat': 38.491226, 'lon': -80.954456},
    'Wisconsin': {'lat': 44.268543, 'lon': -89.616508},
    'Wyoming': {'lat': 42.755966, 'lon': -107.302490}
}

states_list = ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 
               'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 
               'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 
               'VA', 'WA', 'WV', 'WI', 'WY']

# Function to create a Kafka consumer
def create_kafka_consumer(topic_name):
    # Set up a Kafka consumer with specified topic and configurations
    consumer = KafkaConsumer(
        topic_name,
        bootstrap_servers='localhost:9092',
        auto_offset_reset='earliest',
        value_deserializer=lambda x: json.loads(x.decode('utf-8')))
    return consumer

# Function to fetch voting statistics from PostgreSQL database
@st.cache_data
def fetch_voting_stats(): # fix 
    # Connect to PostgreSQL database
    conn = psycopg2.connect("host=localhost dbname=voting user=postgres password=postgres")
    cur = conn.cursor()

    # Fetch total number of voters
    cur.execute("""
        SELECT count(*) voters_count FROM voters
    """)
    voters_count = cur.fetchone()[0]

    # Fetch total number of candidates
    cur.execute("""
        SELECT count(*) candidates_count FROM candidates
    """)
    candidates_count = cur.fetchone()[0]

    return voters_count, candidates_count

# Function to fetch data from Kafka
def fetch_data_from_kafka(consumer): # fix 
    # Poll Kafka consumer for messages within a timeout period
    messages = consumer.poll(timeout_ms=1000)
    data = []

    # Extract data from received messages
    for message in messages.values():
        for sub_message in message:
            data.append(sub_message.value)
    return data

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

# Function to split a dataframe into chunks for pagination
@st.cache_data(show_spinner=False)
def split_frame(input_df, rows):
    df = [input_df.loc[i: i + rows - 1, :] for i in range(0, len(input_df), rows)]
    return df

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
    location_data['state_name'] = states_list

    # Create the figure
    fig = go.Figure()

    # Add a choropleth layer for the state colors
    fig.add_trace(go.Choropleth(
        locationmode="USA-states",
        locations=location_data['state_name'],  # State abbreviations
        z=location_data['count'],   
        zmin=0,                           # Set minimum value for the color scale
        zmax=100,       # Data to color states
            colorscale=[
            [0, "blue"],  # Count <= 50 -> Blue
            [0.5, "blue"],
            [0.5, "red"], # Count > 50 -> Red
            [1, "red"]
        ],
        colorbar_title="Count"
    ))

    # Add state labels directly on the map
    fig.add_trace(go.Scattergeo(
        locationmode="USA-states",
        lat=location_data['latitude'],
        lon=location_data['longitude'],
        text=location_data.apply(lambda row: f"{row['state_name']}<br>votes: {row['count']}", axis=1),
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
# Function to update data displayed on the dashboard
def update_data():
    # Placeholder to display last refresh time
    last_refresh = st.empty()
    last_refresh.text(f"Last refreshed at: {time.strftime('%Y-%m-%d %H:%M:%S')}")

    # Fetch voting statistics
    voters_count, candidates_count = fetch_voting_stats()

    # Display total voters and candidates metrics
    st.markdown("""---""")
    col1, col2 = st.columns(2)
    col1.metric("Total Voters", voters_count)
    col2.metric("Total Candidates", candidates_count)

    # Fetch data from Kafka on aggregated votes per candidate
    consumer = create_kafka_consumer("aggregated_votes_per_candidate")
    data = fetch_data_from_kafka(consumer)
    results = pd.DataFrame(data)

    # Identify the leading candidate
    results = results.loc[results.groupby('candidate_id')['total_votes'].idxmax()]
    leading_candidate = results.loc[results['total_votes'].idxmax()]

    # Display leading candidate information
    st.markdown("""---""")
    st.header('Leading Candidate')
    col1, col2 = st.columns(2)
    with col1:
        st.image(leading_candidate['photo_url'], width=200)
    with col2:
        st.header(leading_candidate['candidate_name'])
        st.subheader(leading_candidate['party_affiliation'])
        st.subheader("Total Vote: {}".format(leading_candidate['total_votes']))

    # Display statistics and visualizations
    st.markdown("""---""")
    st.header('Statistics')
    results = results[['candidate_id', 'candidate_name', 'party_affiliation', 'total_votes']]
    results = results.reset_index(drop=True)
    col1, col2 = st.columns(2)


    # Display bar chart and donut chart
    with col1:
        bar_fig = plot_colored_bar_chart(results)
        st.pyplot(bar_fig)

    with col2:
        donut_fig = plot_donut_chart(results, title='Vote Distribution')
        st.pyplot(donut_fig)

    # Display table with candidate statistics
    st.table(results)

    # Fetch data from Kafka on aggregated turnout by location
    location_consumer = create_kafka_consumer("aggregated_turnout_by_location")
    location_data = fetch_data_from_kafka(location_consumer)
    location_result = pd.DataFrame(location_data)

    # Identify locations with maximum turnout
    location_result = location_result.loc[location_result.groupby('state')['count'].idxmax()]
    location_result = location_result.reset_index(drop=True)

    # Display location-based voter information with pagination
    st.header("Location of Voters")
    paginate_table(location_result)

    # Display the US map with voting data
    st.header("Vote Distribution by State")
    us_map_fig = plot_full_us_map(location_result)
    st.plotly_chart(us_map_fig, use_container_width=True)

    # Update the last refresh time
    st.session_state['last_update'] = time.time()

# Sidebar layout
def sidebar():
    # Initialize last update time if not present in session state
    if st.session_state.get('last_update') is None:
        st.session_state['last_update'] = time.time()

    # Slider to control refresh interval
    refresh_interval = st.sidebar.slider("Refresh interval (seconds)", 5, 60, 10)
    st_autorefresh(interval=refresh_interval * 1000, key="auto")

    # Button to manually refresh data
    if st.sidebar.button('Refresh Data'):
        update_data()

# Title of the Streamlit dashboard
st.title('Real-time Election Dashboard')

# Display sidebar
sidebar()

# Update and display data on the dashboard
update_data()