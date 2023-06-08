import numpy as np
import pygame
import random

# Initialize pygame
pygame.init()

# Set up the display
width, height = 820, 820
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("SPLOOSH KABOOM")

# Define colors
BLUE = (43, 101, 236)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)

# Define grid parameters
grid_size = 20
tile_size = 40
grid_padding = 10

# Create the game grid
grid = np.zeros((grid_size, grid_size), dtype=int)

# Define ship sizes
ship_sizes = [4, 4, 4, 3, 3, 2]

# Place ships on the grid
for size in ship_sizes:
    valid = False
    while not valid:
        x = random.randint(0, grid_size - 1)
        y = random.randint(0, grid_size - 1)
        orientation = random.choice(["horizontal", "vertical"])

        if orientation == "horizontal":
            if y + size <= grid_size and np.count_nonzero(grid[x, y:y + size]) == 0:
                grid[x, y:y + size] = 1
                valid = True
        else:
            if x + size <= grid_size and np.count_nonzero(grid[x:x + size, y]) == 0:
                grid[x:x + size, y] = 1
                valid = True

# Initialize hit count and ships sunk
hit_count = 0
ships_sunk = 0

# Initialize font for printing hits or misses
font = pygame.font.Font(None, 36)

# Game loop
running = True
print("hey welcome to SPLOOSH KABOOM your goal is to find all 6 ships and sink them ")
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and ships_sunk < 6:
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                col = (pos[0] - grid_padding) // tile_size
                row = (pos[1] - grid_padding) // tile_size

                if grid[row][col] == 1:
                    hit_count += 1
                    grid[row][col] = -1
                    if hit_count >= 4:
                        ships_sunk += 1
                        hit_count = 0
                        if ships_sunk == 6:
                            running = False
                            print("Congratulations! You sunk all the ships!")
                    print("KABOOM!")
                elif grid[row][col] == 0:
                    grid[row][col] = -2
                    print("sploosh...")

    # Clear the screen
    screen.fill(BLUE)

    # Draw the grid
    for row in range(grid_size):
        for col in range(grid_size):
            x = col * tile_size + grid_padding
            y = row * tile_size + grid_padding
            pygame.draw.rect(screen, BLUE, (x, y, tile_size, tile_size), 1)

            if grid[row][col] == -1:
                pygame.draw.rect(screen, GREEN, (x + 1, y + 1, tile_size - 2, tile_size - 2))
            elif grid[row][col] == -2:
                pygame.draw.rect(screen, RED, (x + 1, y + 1, tile_size - 2, tile_size - 2))

    # Update the display
    pygame.display.flip()

# Quit the game
pygame.quit()
