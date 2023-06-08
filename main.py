import numpy as np
import pygame
import random

pygame.init()

width, height = 820, 820
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("SPLOOSH KABOOM")

BLUE = (43, 101, 236)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

grid_size = 20
tile_size = 40
grid_padding = 10

grid = np.zeros((grid_size, grid_size), dtype=int)

ship_sizes = [4, 4, 4, 3, 3, 2]

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

hit_count = 0
ships_sunk = 0

font = pygame.font.Font(None, 36)

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
                    print("KABOOM!")
                    if hit_count == 20:
                        ships_sunk = 6
                        if ships_sunk == 6:
                            running = False
                            print("Congratulations! You sunk all the ships!")
                     
                elif grid[row][col] == 0:
                    grid[row][col] = -2
                    print("sploosh...")

    screen.fill(BLUE)

    for row in range(grid_size):
        for col in range(grid_size):
            x = col * tile_size + grid_padding
            y = row * tile_size + grid_padding
            pygame.draw.rect(screen, BLUE, (x, y, tile_size, tile_size), 1)

            if grid[row][col] == -1:
                pygame.draw.rect(screen, GREEN, (x + 1, y + 1, tile_size - 2, tile_size - 2))
            elif grid[row][col] == -2:
                pygame.draw.rect(screen, RED, (x + 1, y + 1, tile_size - 2, tile_size - 2))

    pygame.display.flip()

pygame.quit()

