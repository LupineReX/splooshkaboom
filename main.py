import numpy as np
import pygame
import random

pygame.init() #where the pygame grid starts 

width, height = 820, 820 #following 3 lines control the width and height of the pygame window and the name of the window 
screen = pygame.display.set_mode((width, height)) 
pygame.display.set_caption("SPLOOSH KABOOM")

BLUE = (43, 101, 236) #these three colors are used to generate colors within the 20x20 grid
RED = (255, 0, 0)
GREEN = (0, 255, 0)

grid_size = 20 #controls grid size 
tile_size = 40
grid_padding = 10

grid = np.zeros((grid_size, grid_size), dtype=int)

ship_sizes = [4, 4, 4, 3, 3, 2] #list of the amount of ships plus their varying sizes (three 4 tile ships, two three tile ships, and one 2 tile ship)

for size in ship_sizes:
    valid = False
    while not valid:
        x = random.randint(0, grid_size - 1)
        y = random.randint(0, grid_size - 1) #chooses a random general area of where a ship can be
        orientation = random.choice(["horizontal", "vertical"]) #randomly decides if the ship will be vertical or horziontal 

        if orientation == "horizontal": #aligns ship to be  horziontal 
            if y + size <= grid_size and np.count_nonzero(grid[x, y:y + size]) == 0:
                grid[x, y:y + size] = 1 
                valid = True
        else: #aligns ship to be vertical 
            if x + size <= grid_size and np.count_nonzero(grid[x:x + size, y]) == 0:
                grid[x:x + size, y] = 1
                valid = True

hit_count = 0
ships_sunk = 0
totalclicks = 0  #these three variables track variables that will change throughout the loop
font = pygame.font.Font(None, 36)

running = True #as long as running is true the code will run 
print("hey welcome to SPLOOSH KABOOM your goal is to find all 6 ships and sink them ") 
while running: #code is in a while true loop until win condition is met
    for event in pygame.event.get():
        if event.type == pygame.QUIT: 
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and ships_sunk < 6:
            if pygame.mouse.get_pressed()[0]: #code registers player's click and finds the row and col where the player clicked
                pos = pygame.mouse.get_pos() 
                col = (pos[0] - grid_padding) // tile_size
                row = (pos[1] - grid_padding) // tile_size
                try:
                    if grid[row][col] == 1: #using the value of row and col where the player click if it equals to 1 that means the player hit a ship
                        hit_count += 1
                        grid[row][col] = -1 
                        totalclicks += 1
                        print("KABOOM!")
                    if hit_count == 20: #when hit count is 20 (the total amount of hits when you add all the ship totals together ) playe meets win condition 
                            ships_sunk = 6 
                            if ships_sunk == 6:
                                running = False
                                print("Congratulations! You sunk all the ships!")
                                print("it took ya" + str(totalclicks)+ " clicks.")
                    elif grid[row][col] == 0: #when the value of row and grid make a 0 it means the player missed 
                        grid[row][col] = -2
                        print("sploosh...")
                        totalclicks += 1
                except: #when player clicks out of bounds usually an error happens but using try and execept makes it so it doesn't break this is a temp solution until i find a way to fix it
                    print("ERROR: Out Of Bounds. That wasn't very splash kaboomy of you")
    screen.fill(BLUE) #makes the default grid all blue 

    for row in range(grid_size):
        for col in range(grid_size): 
            x = col * tile_size + grid_padding
            y = row * tile_size + grid_padding
            pygame.draw.rect(screen, BLUE, (x, y, tile_size, tile_size), 1)

            if grid[row][col] == -1: #when ship is hit marked with green tile 
                pygame.draw.rect(screen, GREEN, (x + 1, y + 1, tile_size - 2, tile_size - 2))
            elif grid[row][col] == -2: #when ship is missed marked with red tile 
                pygame.draw.rect(screen, RED, (x + 1, y + 1, tile_size - 2, tile_size - 2))

    pygame.display.flip()

pygame.quit()

