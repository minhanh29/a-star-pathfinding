import pygame
from Colors import Color
from Cell import Cell
from queue import PriorityQueue


WIDTH = 500
SIZE = 50
GAP = WIDTH // SIZE
window = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding")
clock = pygame.time.Clock()


def draw(window, width, size, grid):
    window.fill(Color.WHITE)

    # draw cells
    for row in grid:
        for cell in row:
            cell.draw(window)

    # draw grid line
    gap = width / size
    for row in range(size):
        for col in range(size):
            y = row * gap
            pygame.draw.line(window, Color.GREY, (0, y), (width, y))
            x = col * gap
            pygame.draw.line(window, Color.GREY, (x, 0), (x, width))

    pygame.display.update()


# generate the initial grid of cells
def make_grid(size, gap):
    grid = []
    for i in range(size):
        row = []
        for j in range(size):
            row.append(Cell(i, j, gap))
        grid.append(row)
    return grid


# return the cell coordinate that the mouse is pressing on
def hover_cell(mouse_pos):
    col = mouse_pos[0] // GAP
    row = mouse_pos[1] // GAP
    return grid[row][col]


# the path finding algorithm
def a_star(grid, start, goal, draw):
    goal_pos = goal.get_pos()
    size = len(grid)
    count = 0

    start.f_score = h(start.get_pos(), goal_pos)
    start.g_score = 0

    open_set = PriorityQueue()
    open_set.put((0, count, start))
    count += 1

    # update neighbors
    for row in grid:
        for cell in row:
            cell.update_neighbors(grid, size)

    while not open_set.empty():
        # exit the loop
        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            pygame.quit()

        current = open_set.get()[2]

        # get to the goal
        if current == goal:
            mark_path(start, goal)
            return True

        for cell in current.neighbors:
            g = current.g_score + 1
            if g < cell.g_score:
                # update scores
                cell.g_score = g
                cell.f_score = g + h(cell.get_pos(), goal_pos)
                cell.previous_cell = current

                # cell is not closed
                if not cell.is_closed():
                    open_set.put((cell.f_score, count, cell))
                    count += 1

                    if cell != goal:
                        cell.make_open()

        if current != start:
            current.make_closed()

        draw()

    return False


# draw the path
def mark_path(start, goal):
    current = goal.previous_cell
    while current != start:
        current.make_path()
        current = current.previous_cell


# heuristic function
def h(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


# draw mode: 1 - start, 2 - goal, 3- obstacle, 4 - erase
mode = 3

# make grid
grid = make_grid(SIZE, GAP)

run = True
while run:
    # clock.tick(24)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # mouse press
    if pygame.mouse.get_pressed(3)[0]:
        mouse_pos = pygame.mouse.get_pos()
        cell = hover_cell(mouse_pos)
        cell.recolor(mode)

    draw(window, WIDTH, SIZE, grid)

    # key press
    keys = pygame.key.get_pressed()

    # start mode
    if keys[pygame.K_s]:
        mode = 1

    if keys[pygame.K_g]:
        mode = 2

    if keys[pygame.K_b]:
        mode = 3

    if keys[pygame.K_e]:
        mode = 4

    # start algorithm
    if keys[pygame.K_a] and Cell.start and Cell.goal:
        a_star(grid, Cell.start, Cell.goal,
               lambda: draw(window, WIDTH, SIZE, grid))

    # clear screen
    if keys[pygame.K_c]:
        grid = make_grid(SIZE, GAP)

    if keys[pygame.K_ESCAPE]:
        run = False

pygame.quit()
