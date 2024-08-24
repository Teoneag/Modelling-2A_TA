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
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

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

# Button properties
button_font = pygame.font.Font(None, 36)
button_width, button_height = 150, 50
start_button_pos = (50, 500)
stop_button_pos = (250, 500)
restart_button_pos = (450, 500)

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
        
        # Display the number of cars on the edge if traffic_data is provided
        if traffic_data:
            mid_point = (
                (node_positions[start][0] + node_positions[end][0]) // 2,
                (node_positions[start][1] + node_positions[end][1]) // 2
            )
            cars_on_edge = traffic_data.get(edge, 0)
            font = pygame.font.Font(None, 36)
            text = font.render(str(cars_on_edge), True, RED)
            screen.blit(text, mid_point)

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
    draw_button("Start", start_button_pos, GREEN)
    draw_button("Stop", stop_button_pos, RED)
    draw_button("Reset", restart_button_pos, GRAY)

    pygame.display.flip()

# Main loop to animate traffic based on the log data
running = True
paused = True  # Start in paused state
index = 0
clock = pygame.time.Clock()

# Initial draw to avoid black screen
draw_graph()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos

            # Start button
            if is_inside(mouse_pos, (*start_button_pos, button_width, button_height)):
                paused = False

            # Stop button
            if is_inside(mouse_pos, (*stop_button_pos, button_width, button_height)):
                paused = True

            # Restart button
            if is_inside(mouse_pos, (*restart_button_pos, button_width, button_height)):
                index = 0
                paused = True
                draw_graph()  # Immediately redraw the initial state
                pygame.display.flip()  # Force update of the display
                time.sleep(0.1)  # Brief pause to ensure the reset is visible

    # Update and draw the graph only if not paused
    if not paused and index < len(df_traffic_log):
        traffic_data = df_traffic_log.iloc[index].to_dict()
        draw_graph(traffic_data)
        index += 1
        time.sleep(0.1)  # Delay for animation effect

    clock.tick(60)  # Control the frame rate

pygame.quit()
