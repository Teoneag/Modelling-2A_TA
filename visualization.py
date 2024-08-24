import pygame
import pandas as pd

# Pygame setup
pygame.init()

# Screen dimensions
width, height = 1000, 600
screen = pygame.display.set_mode((width, height))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Frame rate
clock = pygame.time.Clock()
fps = 30

# Load data from the Excel file
df = pd.read_excel("test.xlsx", sheet_name="Sheet4")
# Assuming df has columns 'Vehicle ID', 'Time', 'Position'

# Mapping nodes to screen coordinates (example)
node_positions = {
    "1": (100, 300),
    "A": (300, 200),
    "B": (300, 400),
    "C": (500, 300),
    "D": (700, 200),
    "E": (700, 400),
    "2": (900, 300),
}

# Vehicle data storage (could be improved)
vehicle_positions = {}

# Main loop
running = True
time_step = 1  # Start time

while running:
    screen.fill(WHITE)  # Clear screen
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Draw edges
    pygame.draw.line(screen, BLACK, node_positions["1"], node_positions["A"], 5)
    pygame.draw.line(screen, BLACK, node_positions["1"], node_positions["B"], 5)
    pygame.draw.line(screen, BLACK, node_positions["A"], node_positions["C"], 5)
    pygame.draw.line(screen, BLACK, node_positions["B"], node_positions["C"], 5)
    pygame.draw.line(screen, BLACK, node_positions["C"], node_positions["D"], 5)
    pygame.draw.line(screen, BLACK, node_positions["C"], node_positions["E"], 5)
    pygame.draw.line(screen, BLACK, node_positions["D"], node_positions["2"], 5)
    pygame.draw.line(screen, BLACK, node_positions["E"], node_positions["2"], 5)

    # Draw nodes
    for node, pos in node_positions.items():
        pygame.draw.circle(screen, BLACK, pos, 10)
        font = pygame.font.Font(None, 36)
        text = font.render(node, True, BLACK)
        screen.blit(text, (pos[0] + 15, pos[1] - 15))
    
    # Update vehicle positions
    current_positions = df[df['Time'] == time_step]
    for _, row in current_positions.iterrows():
        vehicle_id = row['Vehicle ID']
        position = row['Position']
        
        if position in node_positions:
            vehicle_positions[vehicle_id] = node_positions[position]
    
    # Draw vehicles
    for pos in vehicle_positions.values():
        pygame.draw.circle(screen, RED, pos, 5)
    
    # Update the display
    pygame.display.flip()
    
    # Increment time step and control frame rate
    time_step += 1
    clock.tick(fps)
    
    # Stop the loop after the last time step
    if time_step > df['Time'].max():
        running = False

pygame.quit()
