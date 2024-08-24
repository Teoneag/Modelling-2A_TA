import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Traffic Simulation")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

# Clock for FPS
clock = pygame.time.Clock()

# Node positions
nodes = {
    'A': (100, 100),
    'B': (700, 100),
    'C': (400, 300),
    'D': (100, 500),
    'E': (700, 500),
}

# Edges connecting nodes (bi-directional)
edges = [
    ('A', 'B'),
    ('A', 'C'),
    ('B', 'C'),
    ('C', 'D'),
    ('C', 'E'),
    ('D', 'E'),
]

# Car class
class Car:
    def __init__(self, start_node, end_node, color=RED):
        self.start_node = start_node
        self.end_node = end_node
        self.color = color
        self.position = list(nodes[start_node])
        self.target_position = list(nodes[end_node])
        self.speed = 2

    def move(self):
        # Calculate direction vector
        direction = [self.target_position[0] - self.position[0], self.target_position[1] - self.position[1]]
        distance = math.hypot(*direction)
        
        if distance == 0:
            return
        
        direction = [direction[0] / distance, direction[1] / distance]
        
        # Move car
        self.position[0] += direction[0] * self.speed
        self.position[1] += direction[1] * self.speed

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.position[0]), int(self.position[1])), 10)

    def reached_target(self):
        return math.hypot(self.target_position[0] - self.position[0], self.target_position[1] - self.position[1]) < self.speed

# Generate random cars
def generate_random_car():
    start_node = random.choice(list(nodes.keys()))
    end_node = random.choice([node for node in nodes if node != start_node])
    return Car(start_node, end_node)

# List of cars
cars = [generate_random_car() for _ in range(5)]

# Main loop
running = True
while running:
    screen.fill(WHITE)
    
    # Draw nodes
    for node, pos in nodes.items():
        pygame.draw.circle(screen, BLACK, pos, 20)
        label = pygame.font.SysFont(None, 24).render(node, True, WHITE)
        screen.blit(label, (pos[0] - label.get_width() // 2, pos[1] - label.get_height() // 2))
    
    # Draw edges
    for edge in edges:
        pygame.draw.line(screen, GRAY, nodes[edge[0]], nodes[edge[1]], 5)

    # Move and draw cars
    for car in cars:
        car.move()
        car.draw(screen)
        if car.reached_target():
            # When a car reaches its destination, give it a new random destination
            car.start_node = car.end_node
            car.end_node = random.choice([node for node in nodes if node != car.start_node])
            car.target_position = list(nodes[car.end_node])

    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    clock.tick(60)

pygame.quit()
