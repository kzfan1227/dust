import pandas as pd
import plotly.express as px

# Load the data
data = pd.read_csv('events_datacol.csv')

# Group data by latitude, longitude, and event type, then count occurrences
location_event_counts = data.groupby(['Latitude', 'Longitude', 'event']).size().reset_index(name='counts')

# Filter out 'Other' events
filtered_data = location_event_counts[location_event_counts['event'] != 'Other']

# Define a color map corresponding to the event types
color_map = {
    "Fire": 'orange',
    "Large Windblown Dust": 'brown',
    "Mild Windblown Dust": 'yellow'
}
filtered_data['color'] = filtered_data['event'].map(color_map)

# Create a scatter mapbox plot
fig = px.scatter_mapbox(filtered_data,
                        lat="Latitude",
                        lon="Longitude",
                        color="event",
                        size="counts",
                        color_discrete_map=color_map,
                        size_max=20,
                        hover_name="event",
                        hover_data={"counts": True, "Latitude": False, "Longitude": False},
                        title="Map of Environmental Events")

# Update the layout to use OpenStreetMap style and set the zoom level
fig.update_layout(mapbox_style="open-street-map", mapbox_zoom=3,
                  mapbox_center = {"lat": 37.0902, "lon": -95.7129})  # Center on the US
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig.show()
