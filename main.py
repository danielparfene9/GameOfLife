import pygame
import numpy as np

# Set up the display
pygame.init()
width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Conway's Game of Life")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Set up grid
n_rows, n_cols = 50, 50
cell_width, cell_height = width // n_cols, height // n_rows
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
    screen.fill(WHITE)
    for x in range(n_cols):
        for y in range(n_rows):
            if grid[x, y] == 1:
                pygame.draw.rect(screen, BLACK, (x * cell_width, y * cell_height, cell_width, cell_height))
    pygame.display.flip()

# Function to update grid based on Conway's rules
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
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    x, y = event.pos
                    grid_x, grid_y = x // cell_width, y // cell_height
                    grid[grid_x, grid_y] = 1
                    drawing = True
            elif event.type == pygame.MOUSEMOTION:
                if drawing:
                    x, y = event.pos
                    grid_x, grid_y = x // cell_width, y // cell_height
                    grid[grid_x, grid_y] = 1
            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    generations = int(input("Enter the number of generations: "))
                    for _ in range(generations):
                        grid = update_grid()
                        draw_grid()
                        pygame.time.wait(100)  # Adjust the speed of the simulation
        draw_grid()
        clock.tick(60)


if __name__ == "__main__":
    main()
