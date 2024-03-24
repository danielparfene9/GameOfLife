import pygame
import numpy as np
import math
import pygame as pg
from constants import *
from inputModel import InputModel
from buttons import Button

# Set up the display
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Conway's Game of Life")

# Set up grid
cell_width, cell_height = width // n_cols, height // n_rows
grid = np.zeros((n_rows, n_cols))
friendly_zone = np.zeros((n_rows, n_cols))


# Function to count neighbors
def count_neighbors(x, y):
    neighbor_count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not (i == 0 and j == 0):
                neighbor_x = (x + i + n_cols) % n_cols
                neighbor_y = (y + j + n_rows) % n_rows
                neighbor_count += grid[neighbor_x, neighbor_y]
    return neighbor_count


# Function to update grid based on Conway's rules including the friendly neighborhood behavior
def update_grid(friendly_zone):
    new_grid = np.copy(grid)
    for x in range(n_cols):
        for y in range(n_rows):
            cell_neighbors = count_neighbors(x, y)
            if grid[x, y] == 1:
                if cell_neighbors < 2 or cell_neighbors > 3:
                    new_grid[x, y] = 0
            else:
                if cell_neighbors == 3:
                    new_grid[x, y] = 1
                # Implementing the Friendly Neighborhood behavior
                if friendly_zone[x, y] == 1 and cell_neighbors < 2:
                    # Check if there are other living cells nearby
                    other_neighbors = count_neighbors(x, y)
                    if other_neighbors > 0:
                        new_grid[x, y] = 1
    return new_grid


# Function to draw grid including the friendly zone
def draw_grid():
    for x in range(n_cols):
        for y in range(n_rows):
            # Draw friendly zone cells with light green color and opacity 0.5
            if friendly_zone[x, y] == 1:
                pygame.draw.rect(screen, (144, 238, 144, 128),
                                 (x * cell_width, y * cell_height, cell_width, cell_height))
            elif grid[x, y] == 1:
                pygame.draw.rect(screen, BLACK, (x * cell_width, y * cell_height, cell_width, cell_height))
    pygame.display.flip()


# Main function to run the simulation
def main():
    global grid, friendly_zone
    drawing = False
    clock = pygame.time.Clock()
    input_field = InputModel(screen=screen, x=3 * width / 8, y=7.4 * height / 8, w=2 * width / 8, h=height / 16,
                             text_color=None, box_color=None)
    next_button = Button(screen=screen, color=WHITE, x=6 * width / 9, y=7 * height / 8, tipe="next", radius=30)
    prev_button = Button(screen=screen, color=WHITE, x=3 * width / 9, y=7 * height / 8, tipe="previous", radius=30)
    stop_button = Button(screen=screen, color=WHITE, x=4 * width / 9, y=7 * height / 8, tipe="stop", radius=30)
    play_button = Button(screen=screen, color=WHITE, x=5 * width / 9, y=7 * height / 8, tipe="play", radius=30)

    while True:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                input_field.isPressed(event)
                if event.button == 1 and event.pos[1] < 6 * height / 8:
                    x, y = event.pos
                    grid_x, grid_y = x // cell_width, y // cell_height
                    grid[grid_x, grid_y] = 1
                    drawing = True
            elif event.type == pygame.MOUSEMOTION:
                if drawing and event.pos[1] < 6 * height / 8:
                    x, y = event.pos
                    grid_x, grid_y = x // cell_width, y // cell_height
                    grid[grid_x, grid_y] = 1
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
            elif event.type == pygame.KEYDOWN:
                input_field.changeText(event)

        # Update friendly zone based on mouse clicks (assuming left mouse button)
        mouse_pos = pygame.mouse.get_pos()
        if pygame.mouse.get_pressed()[0] and mouse_pos[1] < 6 * height / 8:
            x, y = mouse_pos
            grid_x, grid_y = x // cell_width, y // cell_height
            friendly_zone[grid_x, grid_y] = 1

        input_field.draw()
        next_button.draw()
        prev_button.draw()
        stop_button.draw()
        play_button.draw()

        # Update the grid with friendly zone included
        grid = update_grid(friendly_zone)

        # Draw the grid
        draw_grid()

        clock.tick(60)


if __name__ == "__main__":
    main()
