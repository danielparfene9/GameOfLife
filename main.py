import pygame
import numpy as np

from inputModel import InputModel
from buttons import Button
from constants import *

# Set up the display
pygame.init()
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Conway's Game of Life")

# Set up grid
cell_width, cell_height = width // n_cols, int(3*height/4) // n_rows
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
                pygame.draw.rect(screen, BLACK, (x * cell_width, y * cell_height, cell_width, cell_height))
            else:
                pygame.draw.rect(screen, WHITE, (x * cell_width, y * cell_height, cell_width, cell_height))
        pygame.draw.line(screen, BLACK, (x*cell_width, 0), (x*cell_width, int(3*height/4)))

    for y in range(n_rows+1):
        pygame.draw.line(screen, BLACK, (0, y * cell_height), (width, y * cell_height))

    pygame.display.flip()


def update_grid():
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
    return new_grid


# Main function to run the simulation
def main():
    global grid
    drawing = False
    pause = False
    current_gen = 0
    clock = pygame.time.Clock()
    input_field = InputModel(screen=screen, x=3*width/8, y=7.4*height/8, w=2*width/8, h=height / 16, text_color=None, box_color=None)
    next_button = Button(screen=screen, color=WHITE, x=3*width/4, y=7*height/8, tipe="next", radius=30)
    prev_button = Button(screen=screen, color=WHITE, x=width/4, y=7*height/8, tipe="previous", radius=30)
    stop_button = Button(screen=screen, color=WHITE, x=width/2, y=7*height/8, tipe="play", radius=30)

    while True:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                input_field.isPressed(event)

                if stop_button.isPressed(event.pos[0], event.pos[1]):
                    pause = not pause
                    stop_button.switch_button()

                if event.button == 1 and event.pos[1] < 6*height/8:
                    x, y = event.pos
                    grid_x, grid_y = x // cell_width, y // cell_height
                    grid[grid_x, grid_y] = 1
                    drawing = True
            elif event.type == pygame.MOUSEMOTION:
                if drawing and event.pos[1] < 6*height/8:
                    x, y = event.pos
                    grid_x, grid_y = x // cell_width, y // cell_height
                    grid[grid_x, grid_y] = 1
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
            elif event.type == pygame.KEYDOWN:
                input_field.changeText(event)

            if pause and len(input_field.user_text) > 0:
                print(current_gen)
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
        pygame.time.wait(100)
        clock.tick(60)


if __name__ == "__main__":
    main()
