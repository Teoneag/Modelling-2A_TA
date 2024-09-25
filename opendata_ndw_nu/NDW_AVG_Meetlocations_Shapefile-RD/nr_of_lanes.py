# data from https://opendata.ndw.nu/NDW_AVG_Meetlocaties_Shapefile.zip

import geopandas as gpd

# Load the shapefile
shapefile_path = 'opendata_ndw_nu/NDW_AVG_Meetlocations_Shapefile-RD/Meetvakken_WGS84.shp'
gdf = gpd.read_file(shapefile_path)

print("Available columns:", gdf.columns)