# used https://downloads.rijkswaterstaatdata.nl/wkd/Maximum%20Snelheden/01-01-2023/
# only contains maxspeed, no nr of lanes

import geopandas as gpd

# Load the shapefile
gdf = gpd.read_file('opendata_ndw_nu/max_speed/Snelheden.shp')

# Display the first 10 rows to understand the structure
first_10_rows = gdf.head(10)
print(first_10_rows)

# Print the column names
print("Available columns:", gdf.columns)

# Use MAXSHD for speed limits
speed_limits = first_10_rows['MAXSHD']  # Speed limits

# Display the data
for speed in speed_limits:
    print(f'Speed Limit: {speed}')

