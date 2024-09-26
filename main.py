# Repo link: https://github.com/Netnet78/3D-Moving-Cube.git
# Import necessary libraries
import pygame
import numpy as np
import keyboard
from math import *

# Constants
WIDTH, HEIGHT = 1200, 800
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Space simulation")

# Define 3D points to project
points = [
    np.matrix([-1, -1, 1]),
    np.matrix([1, -1, 1]),
    np.matrix([1, 1, 1]),
    np.matrix([-1, 1, 1]),
    np.matrix([-1, -1, -1]),
    np.matrix([1, -1, -1]),
    np.matrix([1, 1, -1]),
    np.matrix([-1, 1, -1])
]

# Define projection matrix
projection_matrix = np.matrix([
    [1, 0, 0],
    [0, 1, 0],
    [0, 0, 0]
])

# Define circle properties
scale = 100
circle_pos = [WIDTH / 2, HEIGHT / 2]

# Define rotation angles
angle_x = 90
angle_y = 90
angle_z = 90

# Define translation variables
translate_x = 0
translate_y = 0

# Function to connect points
def connect_points(points):
    """Draw lines between specific points in a 3D cube to form its edges."""
    edges = [
        (0, 1), (1, 2), (2, 3), (3, 0),  # front face
        (4, 5), (5, 6), (6, 7), (7, 4),  # back face
        (0, 4), (1, 5), (2, 6), (3, 7)  # connections between faces
    ]
    for edge in edges:
        pygame.draw.line(screen, BLACK, (points[edge[0]][0], points[edge[0]][1]), (points[edge[1]][0], points[edge[1]][1]), 1)

# Main game loop
clock = pygame.time.Clock()
running = True
auto_spin_u = False
auto_spin_d = False
auto_spin_l = False
auto_spin_r = False
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_UP:
                angle_x -= 10
            elif event.key == pygame.K_DOWN:
                angle_x += 10
            elif event.key == pygame.K_LEFT:
                angle_y -= 10
            elif event.key == pygame.K_RIGHT:
                angle_y += 10
            elif event.key == pygame.K_u:
                auto_spin_u = True
                auto_spin_d = False
            elif event.key == pygame.K_d:
                auto_spin_d = True
                auto_spin_u = False
            elif event.key == pygame.K_l:
                auto_spin_l = True
                auto_spin_r = False
            elif event.key == pygame.K_r:
                auto_spin_r = True
                auto_spin_l = False
            elif event.key == pygame.K_s:
                auto_spin_l = False
                auto_spin_d = False
                auto_spin_r = False
                auto_spin_u = False
        elif event.type == pygame.MOUSEMOTION:
            if event.buttons[0]:
                translate_x += event.rel[0]
                translate_y += event.rel[1]

    screen.fill(WHITE)

    # Auto spin
    if auto_spin_u:
        angle_x -= 1
    if auto_spin_d:
        angle_x += 1
    if auto_spin_l:
        angle_y += 1
    if auto_spin_r:
        angle_y -= 1

    # Rotation matrices
    rotation_z = np.matrix([
        [cos(radians(angle_z)), -sin(radians(angle_z)), 0],
        [sin(radians(angle_z)), cos(radians(angle_z)), 0],
        [0, 0, 1]
    ])

    rotation_y = np.matrix([
        [cos(radians(angle_y)), 0, sin(radians(angle_y))],
        [0, 1, 0],
        [-sin(radians(angle_y)), 0, cos(radians(angle_y))]
    ])

    rotation_x = np.matrix([
        [1, 0, 0],
        [0, cos(radians(angle_x)), -sin(radians(angle_x))],
        [0, sin(radians(angle_x)), cos(radians(angle_x))]
    ])
    # Increase rotation angle
    angle = int((angle_x + angle_y + angle_z) / 3)

    # Project points
    projected_points = []
    for point in points:
        # Rotate point in 2D
        rotated2d_z = np.dot(rotation_z, point.reshape((3, 1)))
        rotated2d_y = np.dot(rotation_y, rotated2d_z)
        rotated2d_x = np.dot(rotation_x, rotated2d_z)
        rotate_vertical = np.dot(rotation_x, point.reshape((3, 1)))
        rotate_horizontal = np.dot(rotation_y, point.reshape((3, 1)))
        project2d = np.dot(projection_matrix, np.dot(rotation_x, rotated2d_y))

        # Calculate screen coordinates
        x = int(project2d[0, 0] * scale) + circle_pos[0] + translate_x
        y = int(project2d[1, 0] * scale) + circle_pos[1] + translate_y

        # Draw point
        pygame.draw.circle(screen, RED, (x, y), 5)

        # Add point to projected points list
        projected_points.append([x, y])

    # Connect points
    connect_points(projected_points)

    # Update display
    pygame.display.update()
