import pandas as pd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

# Load the data
data = pd.read_csv('events_datacol.csv')

# Group data by latitude, longitude, and event type, then count occurrences
location_event_counts = data.groupby(['Latitude', 'Longitude', 'event']).size().reset_index(name='counts')

# Create a plot
fig = plt.figure(figsize=(10, 8))
ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

# Add features to the map
ax.add_feature(cfeature.STATES, linewidth=0.5, edgecolor='gray')
ax.add_feature(cfeature.LAND)
ax.add_feature(cfeature.OCEAN)
ax.add_feature(cfeature.COASTLINE)
ax.add_feature(cfeature.BORDERS, linestyle=':')
ax.add_feature(cfeature.LAKES, alpha=0.5)
ax.add_feature(cfeature.RIVERS)
ax.set_extent([-125, -66.5, 24, 49], ccrs.Geodetic())  # Continental US bounds

# Define colors or markers for each event type
event_colors = {
    "Fire": 'orange',
    "Large Windblown Dust": 'brown',
    "Mild Windblown Dust": 'yellow'
}

# Filter out 'Other' events
filtered_data = location_event_counts[location_event_counts['event'] != 'Other']

# Plot each event type with different colors
for event_type, group_data in filtered_data.groupby('event'):
    ax.scatter(group_data['Longitude'], group_data['Latitude'], s=group_data['counts']*4,
               color=event_colors.get(event_type, 'gray'), label=event_type, alpha=0.7, transform=ccrs.Geodetic())

# Adding Gridlines
gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True,
                  linewidth=1, color='gray', alpha=0.5, linestyle='--')
gl.top_labels = False
gl.right_labels = False

# Add a legend
plt.legend(title='Event Type')

plt.title('Map of Environmental Events')
plt.show()
