import pygame
import pandas as pd
import time

# Load the traffic log and edge capacity data from the previous simulation
df_traffic_log = pd.read_excel("test.xlsx", sheet_name="Traffic Log")
df_edge_info = pd.read_excel("test.xlsx", sheet_name="Sheet3")

# Convert edge_info DataFrame to a dictionary
edge_info = df_edge_info.set_index('Edge').to_dict('index')

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1500, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Traffic Simulation")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Set up node positions with increased distance
node_positions = {
    "1": (int(width * 0.1), int(height * 0.5)),
    "A": (int(width * 0.3), int(height * 0.3)),
    "B": (int(width * 0.3), int(height * 0.7)),
    "C": (int(width * 0.5), int(height * 0.5)),
    "D": (int(width * 0.7), int(height * 0.3)),
    "E": (int(width * 0.7), int(height * 0.7)),
    "2": (int(width * 0.9), int(height * 0.5))
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

# Button properties
button_font = pygame.font.Font(None, 36)
button_width, button_height = 150, 50
start_stop_button_pos = (int(width * 0.05), int(height * 0.9))
step_button_pos = (int(width * 0.3), int(height * 0.9))
step_back_button_pos = (int(width * 0.475), int(height * 0.9))  # New position
restart_button_pos = (int(width * 0.65), int(height * 0.9))  # Adjusted position

# Function to draw buttons
def draw_button(text, position, color):
    pygame.draw.rect(screen, color, (*position, button_width, button_height))
    text_surf = button_font.render(text, True, BLACK)
    screen.blit(text_surf, (position[0] + 20, position[1] + 10))

# Function to check if a point is inside a rectangle
def is_inside(pos, rect):
    x, y = pos
    rx, ry, rw, rh = rect
    return rx <= x <= rx + rw and ry <= y <= ry + rh

# Function to draw the graph
def draw_graph(traffic_data=None):
    screen.fill(WHITE)

    # Draw edges
    for edge, (start, end) in edges.items():
        pygame.draw.line(screen, BLACK, node_positions[start], node_positions[end], 5)
        
        # Display the number of cars on the edge and capacity usage if traffic_data is provided
        if traffic_data:
            cars_on_edge = traffic_data.get(edge, 0)
            capacity = edge_info.get(edge, {}).get('Capacity', 1)  # Retrieve the capacity for the edge
            percentage_used = (cars_on_edge / capacity) * 100
            # Display format: 'cars_on_edge / capacity (percentage%)'
            text = f"{percentage_used:.0f}% ({cars_on_edge} / {capacity})"
            font = pygame.font.Font(None, 36)
            rendered_text = font.render(text, True, RED)
            mid_point = (
                (node_positions[start][0] + node_positions[end][0]) // 2,
                (node_positions[start][1] + node_positions[end][1]) // 2
            )
            screen.blit(rendered_text, mid_point)

    # Draw nodes (vertices)
    for node, pos in node_positions.items():
        pygame.draw.circle(screen, BLUE, pos, 20)

        # Display the number of cars on the vertex if traffic_data is provided
        if traffic_data:
            cars_on_node = traffic_data.get(node, 0)
            font = pygame.font.Font(None, 36)
            text = font.render(str(cars_on_node), True, RED)
            screen.blit(text, (pos[0] + 25, pos[1] - 25))

    # Draw buttons
    draw_button("Start/Stop", start_stop_button_pos, GREEN)
    draw_button("Step forward", step_button_pos, BLUE)
    draw_button("Step Back", step_back_button_pos, BLUE)  # Blue button
    draw_button("Reset", restart_button_pos, GRAY)

    pygame.display.flip()

# Main loop to animate traffic based on the log data
running = True
paused = True
index = 0
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            # Start/Stop button
            if is_inside(mouse_pos, (*start_stop_button_pos, button_width, button_height)):
                paused = not paused

            # Step button
            if is_inside(mouse_pos, (*step_button_pos, button_width, button_height)):
                if index < len(df_traffic_log):
                    index += 1

            # Step Back button
            if is_inside(mouse_pos, (*step_back_button_pos, button_width, button_height)):
                if index > 0:
                    index -= 1

            # Restart button
            if is_inside(mouse_pos, (*restart_button_pos, button_width, button_height)):
                index = 0
                paused = True

    traffic_data = df_traffic_log.iloc[index].to_dict()
    draw_graph(traffic_data)

    if not paused and index < len(df_traffic_log):
        index += 1
        time.sleep(0.1)

    clock.tick(60) 

pygame.quit()
