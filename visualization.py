import pygame
import pandas as pd
import time
import math

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
PURPLE = (208, 204, 252)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)
ORANGE = (255, 132, 4)

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
button_width, button_height = 190, 50
large_space = 155
small_space = 40

# Slider properties
slider_width = 200
slider_height = 10
slider_handle_width = 20
slider_min_speed = 0.01  # Minimum sleep time (faster simulation)
slider_max_speed = 1.0  # Maximum sleep time (slower simulation)
slider_range = slider_max_speed - slider_min_speed
slider_handle_radius = slider_handle_width // 2

# Calculate slider and button positions
start_stop_button_pos = (int(width * 0.05), int(height * 0.9))
step_back_button_pos = (start_stop_button_pos[0] + button_width + large_space, int(height * 0.9))
step_button_pos = (step_back_button_pos[0] + button_width + small_space, int(height * 0.9))
slider_label_pos = (step_button_pos[0] + button_width * 1.5 + small_space, int(height * 0.9) + 20)
restart_button_pos = (slider_label_pos[0] + slider_width // 2 + large_space, int(height * 0.9))
slider_x = slider_label_pos[0] - (slider_width // 2)
slider_y = slider_label_pos[1] + 10
slider_handle_pos = slider_x + slider_width // 2
slider_handle_area = pygame.Rect(slider_x - slider_handle_radius, slider_y - 10 - slider_handle_radius, slider_width + slider_handle_width, slider_height + 20)

def draw_button(text, position, color):
    pygame.draw.rect(screen, color, (*position, button_width, button_height))
    text_surf = button_font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=(position[0] + button_width // 2, position[1] + button_height // 2))
    screen.blit(text_surf, text_rect)

def draw_slider():
    pygame.draw.rect(screen, BLACK, (slider_x, slider_y, slider_width, slider_height))
    pygame.draw.rect(screen, GREEN, (slider_handle_pos - slider_handle_width // 2, slider_y - 10, slider_handle_width, slider_height + 20))

def draw_slider_label():
    label_font = pygame.font.Font(None, 36)
    label_text = label_font.render("Simulation Speed", True, BLACK)
    label_rect = label_text.get_rect(midbottom=(slider_label_pos[0], slider_label_pos[1]))  # Centered and positioned above the slider
    screen.blit(label_text, label_rect)

def get_slider_value():
    return slider_max_speed - (slider_handle_pos - slider_x) / slider_width * slider_range

# Check if a point is inside a rectangle
def is_inside(pos, rect):
    x, y = pos
    rx, ry, rw, rh = rect
    return rx <= x <= rx + rw and ry <= y <= ry + rh

def get_edge_color(percentage_used):
    """
    Calculate the color of the edge based on its traffic usage percentage.
    0% -> green (0, 255, 0)
    100% -> red (255, 0, 0)
    """
    # Interpolate between green and red
    red = int(255 * (percentage_used / 100))
    green = int(255 * (1 - (percentage_used / 100)))
    return (red, green, 0)

def draw_graph(traffic_data=None):
    screen.fill(WHITE)

    # Draw edges
    for edge, (start, end) in edges.items():
        cars_on_edge = traffic_data.get(edge, 0) if traffic_data else 0
        capacity = edge_info.get(edge, {}).get('Capacity', 1)
        percentage_used = (cars_on_edge / capacity) * 100 if capacity > 0 else 0
        
        # Determine the color of the edge based on its usage
        edge_color = get_edge_color(percentage_used)
        
        # Draw the edge with the computed color
        pygame.draw.line(screen, edge_color, node_positions[start], node_positions[end], 5)

        # Draw traffic information text
        text = f"{percentage_used:.0f}% ({cars_on_edge} / {capacity})"
        font = pygame.font.Font(None, 36)
        rendered_text = font.render(text, True, BLACK)

        # Calculate the midpoint and direction vector for text positioning
        start_pos = pygame.math.Vector2(node_positions[start])
        end_pos = pygame.math.Vector2(node_positions[end])
        direction = end_pos - start_pos
        direction.normalize_ip()
        mid_point = start_pos + direction * (start_pos.distance_to(end_pos) / 2)

        # Adjust the position further away from nodes "1" or "2" if they are endpoints
        offset = 0
        if direction.y < 0:  # Upward edge
            offset = 28
        else:  # Downward edge
            offset = 15
        if start in {"1", "2"}:
            mid_point += direction * offset  # Move text further along the edge away from "1" or "2"
        elif end in {"1", "2"}:
            mid_point -= direction * offset  # Move text further along the edge away from "1" or "2"


        # Compute angle to rotate the text
        angle = math.degrees(math.atan2(direction.y, direction.x))
        rotated_text = pygame.transform.rotate(rendered_text, -angle)

        # Position the text slightly away from the line
        text_rect = rotated_text.get_rect(center=mid_point)
        offset = 25
        screen.blit(rotated_text, text_rect.move(0, offset))

    special_nodes = {"1", "2"}

    # Draw nodes (vertices)
    for node, pos in node_positions.items():
        is_special_node = node in special_nodes
        node_color = ORANGE if is_special_node else PURPLE
        node_radius = 80 if is_special_node else 40
        node = "City " + node if is_special_node else node

        # Draw the black outline
        pygame.draw.circle(screen, BLACK, pos, node_radius + 2)
        pygame.draw.circle(screen, node_color, pos, node_radius)

        # Display the node's name and number of cars inside the node
        font = pygame.font.Font(None, 36)
        node_text = font.render(node, True, BLACK)
        cars_text = font.render(str(traffic_data.get(node, 0)), True, RED)

        node_text_rect = node_text.get_rect(center=(pos[0], pos[1] - 10))
        cars_text_rect = cars_text.get_rect(center=(pos[0], pos[1] + 20))

        screen.blit(node_text, node_text_rect)
        screen.blit(cars_text, cars_text_rect)

    # Draw controls
    draw_button("Start/Stop", start_stop_button_pos, GREEN)
    draw_button("Step Forward", step_button_pos, PURPLE)
    draw_button("Step Back", step_back_button_pos, PURPLE)
    draw_slider_label()
    draw_slider()
    draw_button("Reset", restart_button_pos, GRAY)

    pygame.display.flip()


# Main loop to animate traffic based on the log data
running = True
paused = True
index = 0
slider_dragging = False
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

            # Slider handle dragging
            if slider_handle_area.collidepoint(mouse_pos):
                slider_dragging = True
                slider_handle_pos = min(max(mouse_pos[0], slider_x), slider_x + slider_width)

        if event.type == pygame.MOUSEBUTTONUP:
            slider_dragging = False

        if event.type == pygame.MOUSEMOTION:
            if slider_dragging:
                slider_handle_pos = min(max(event.pos[0], slider_x), slider_x + slider_width)

    traffic_data = df_traffic_log.iloc[index].to_dict()
    draw_graph(traffic_data)

    if not paused and index < len(df_traffic_log):
        index += 1
        time.sleep(get_slider_value())

    clock.tick(60)

pygame.quit()
