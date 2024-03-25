import random

import pygame
import numpy as np
from pyvidplayer import Video
from inputModel import InputModel
from buttons import Button
from constants import *

# Set up the display
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Conway's Game of Life")

# Set up grid
cell_width, cell_height = width // n_cols, int(3 * height / 4) // n_rows
grid = np.zeros((n_rows, n_cols))


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


# Function to draw grid
def draw_grid():
    for x in range(n_cols):
        for y in range(n_rows):
            if grid[x, y] == 1:
                pygame.draw.rect(screen, WHITE, (x * cell_width, y * cell_height, cell_width, cell_height))
            else:
                pygame.draw.rect(screen, BLACK, (x * cell_width, y * cell_height, cell_width, cell_height))

    transparent_surface = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)

    deadly_zone_start_x = n_cols // 3 * cell_width
    deadly_zone_end_x = 2 * n_cols // 3 * cell_width
    deadly_zone_start_y = n_rows // 3 * cell_height
    deadly_zone_end_y = 2 * n_rows // 3 * cell_height
    deadly_zone_width = deadly_zone_end_x - deadly_zone_start_x
    deadly_zone_height = deadly_zone_end_y - deadly_zone_start_y

    pygame.draw.rect(transparent_surface, DEADLY_ZONE_COLOR,
                     (deadly_zone_start_x, deadly_zone_start_y, deadly_zone_width, deadly_zone_height))

    screen.blit(transparent_surface, (0, 0))

    pygame.display.flip()


def update_grid():
    new_grid = np.copy(grid)
    for x in range(n_cols):
        for y in range(n_rows):
            cell_neighbors = count_neighbors(x, y)
            in_deadly_zone = is_in_deadly_zone(x, y)
            if grid[x, y] == 1:
                if in_deadly_zone and (cell_neighbors >= 3 or cell_neighbors < 2):
                    print(cell_neighbors)
                    new_grid[x, y] = 0  # Cell dies due to overpopulation in deadly zone
                elif not in_deadly_zone and (cell_neighbors < 2 or cell_neighbors > 3):
                    new_grid[x, y] = 0  # Regular Game of Life rules
            else:
                if cell_neighbors == 3:
                    new_grid[x, y] = 1
    return new_grid


def is_in_deadly_zone(x, y):
    deadly_zone_start_x = n_cols // 3
    deadly_zone_end_x = 2 * n_cols // 3
    deadly_zone_start_y = n_rows // 3
    deadly_zone_end_y = 2 * n_rows // 3

    return (deadly_zone_start_x <= x <= deadly_zone_end_x) and (deadly_zone_start_y <= y <= deadly_zone_end_y)


def apply_center_gravity(grid):
    center_x, center_y = n_rows // 2, n_cols // 2

    if random.random() < 0.3:
        for x in range(n_rows):
            for y in range(n_cols):
                if grid[x, y] == 1:  # Only apply to alive cells
                    move_x, move_y = 0, 0

                    # Determine the direction to move (towards the center)
                    if x < center_x - 1:  # Move down if above center
                        move_x = 1
                    elif x > center_x:  # Move up if below center
                        move_x = -1

                    if y < center_y - 1:  # Move right if left of center
                        move_y = 1
                    elif y > center_y:  # Move left if right of center
                        move_y = -1
                    # Check if the target cell is empty and within bounds
                    new_x, new_y = x + move_x, y + move_y

                    if n_rows > new_x >= 0 == grid[new_x, new_y] and 0 <= new_y < n_cols:
                        # Move cell
                        grid[x, y] = 0
                        grid[new_x, new_y] = 1

    return grid


vid = Video("videos/Intro.mp4")
vid.set_size((800, 800))


def intro():
    while True:
        vid.draw(screen, (0, 0))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                vid.close()
                main()


def main():
    global grid
    drawing = False
    pause = False
    current_gen = 0
    clock = pygame.time.Clock()
    input_field = InputModel(screen=screen, x=3 * width / 8, y=7.4 * height / 8, w=2 * width / 8, h=height / 16,
                             text_color=None, box_color=None)
    next_button = Button(screen=screen, color=WHITE, x=3 * width / 4, y=7 * height / 8, tipe="next", radius=30)
    prev_button = Button(screen=screen, color=WHITE, x=width / 4, y=7 * height / 8, tipe="previous", radius=30)
    stop_button = Button(screen=screen, color=WHITE, x=width / 2, y=7 * height / 8, tipe="play", radius=30)

    while True:
        screen.fill(BACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                input_field.isPressed(event)

                if stop_button.isPressed(event.pos[0], event.pos[1]):
                    pause = not pause
                    stop_button.switch_button()

                if next_button.isPressed(event.pos[0], event.pos[1]):
                    if int(input_field.user_text) > current_gen:
                        grid = update_grid()
                        current_gen += 1

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

            if pause and len(input_field.user_text) > 0:
                if int(input_field.user_text) > current_gen:
                    grid = update_grid()
                    current_gen += 1

                if int(input_field.user_text) == current_gen:
                    pause = not pause
                    stop_button.switch_button()
                    current_gen = 0

        input_field.print_current(str(current_gen))
        input_field.draw()
        next_button.draw()
        prev_button.draw()
        stop_button.draw()

        draw_grid()
        clock.tick(60)


if __name__ == "__main__":
    intro()
