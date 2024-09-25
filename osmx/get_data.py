import osmnx as ox
import matplotlib.pyplot as plt
import time

# Set cache directory (optional, default is your home directory)
ox.config(log_file=True, log_console=True, use_cache=True)

# Start timing
start_time = time.time()

# Get the graph for Delft with caching
print("Fetching graph data for Delft...")
try:
    G = ox.graph_from_place("Delft, Netherlands", network_type='drive')
    print(f"Graph data fetched in {time.time() - start_time:.2f} seconds.")
except Exception as e:
    print(f"Error fetching data: {e}")

# Start timing for projection
print("Projecting graph to UTM...")
start_time = time.time()
G_projected = ox.project_graph(G)
print(f"Graph projected in {time.time() - start_time:.2f} seconds.")

# Start timing for GeoDataFrame conversion
print("Converting graph to GeoDataFrames...")
start_time = time.time()
nodes, edges = ox.graph_to_gdfs(G_projected)
print(f"GeoDataFrames created in {time.time() - start_time:.2f} seconds.")

# Filter edges to get speed limits and number of lanes
print("Filtering edges for speed limits and lane counts...")
start_time = time.time()
edges_filtered = edges[edges['maxspeed'].notnull() & edges['lanes'].notnull()]
print(f"Filtered edges in {time.time() - start_time:.2f} seconds.")
print(f"Number of filtered edges: {len(edges_filtered)}")

# Display number of lanes for each filtered edge
print("Number of lanes for each filtered edge:")
print(edges_filtered[['lanes']])

# Start plotting
print("Plotting the graph...")
fig, ax = ox.plot_graph(G_projected, node_size=0, edge_color='gray', edge_linewidth=0.5)
