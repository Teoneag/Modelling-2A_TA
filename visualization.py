import pygame
import pandas as pd
import time

# Load the traffic log from the previous simulation
df_traffic_log = pd.read_excel("test.xlsx", sheet_name="Traffic Log")

# Initialize Pygame
pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Traffic Simulation")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Set up node positions
node_positions = {
    "1": (100, 300),
    "A": (200, 200),
    "B": (200, 400),
    "C": (400, 300),
    "D": (600, 200),
    "E": (600, 400),
    "2": (700, 300)
}

# Define edges as pairs of nodes
edges = {
    "1_A": ("1", "A"),
    "1_B": ("1", "B"),
    "A_C": ("A", "C"),
    "B_C": ("B", "C"),
    "C_D": ("C", "D"),
    "C_E": ("C", "E"),
    "C_2": ("C", "2"),
    "D_2": ("D", "2"),
    "E_2": ("E", "2")
}

# Function to draw the graph
def draw_graph(traffic_data):
    screen.fill(WHITE)

    # Draw edges
    for edge, (start, end) in edges.items():
        pygame.draw.line(screen, BLACK, node_positions[start], node_positions[end], 5)
        
        # Display the number of cars on the edge
        mid_point = (
            (node_positions[start][0] + node_positions[end][0]) // 2,
            (node_positions[start][1] + node_positions[end][1]) // 2
        )
        cars_on_edge = traffic_data[edge]
        font = pygame.font.Font(None, 36)
        text = font.render(str(cars_on_edge), True, RED)
        screen.blit(text, mid_point)

    # Draw nodes (vertices)
    for node, pos in node_positions.items():
        pygame.draw.circle(screen, BLUE, pos, 20)

        # Display the number of cars on the vertex
        cars_on_node = traffic_data[node]
        font = pygame.font.Font(None, 36)
        text = font.render(str(cars_on_node), True, RED)
        screen.blit(text, (pos[0] + 25, pos[1] - 25))

    pygame.display.flip()

# Main loop to animate traffic based on the log data
running = True
index = 0
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Get the traffic data for the current timestamp
    if index < len(df_traffic_log):
        traffic_data = df_traffic_log.iloc[index].to_dict()
        draw_graph(traffic_data)
        index += 1
        time.sleep(0.1)  # Delay for animation effect

    clock.tick(60)  # Control the frame rate

pygame.quit()
