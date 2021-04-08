from Colors import Color
from pygame.draw import rect


class Cell():
    start = None
    goal = None

    def __init__(self, row, col, gap):
        self.row = row
        self.col = col
        self.gap = gap
        self.x = gap * col
        self.y = gap * row

        self.color = Color.WHITE

        self.f_score = float("inf")
        self.g_score = float("inf")
        self.previous_cell = None
        self.neighbors = []

    # hash
    def __hash__(self):
        return self.row.__hash__() + self.col.__hash__()

    # equal
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    # less than
    def __lt__(self, other):
        return False

    def draw(self, window):
        rect(window, self.color, (self.x, self.y, self.gap, self.gap))

    def mouse_is_over(self, mouse_pos):
        x = mouse_pos[0]
        y = mouse_pos[1]
        if x > self.x and x < self.x + self.gap and\
                y > self.y and y < self.y + self.gap:
            return True
        return False

    def get_pos(self):
        return (self.row, self.col)

    # draw mode: 1 - start, 2 - goal, 3- obstacle, 4 - erase
    def recolor(self, mode):
        # start
        if mode == 1:
            self.make_start()
        # goal
        elif mode == 2:
            self.make_goal()
        # obstacle
        elif mode == 3:
            self.make_obstacle()
        # erase
        elif mode == 4:
            self.make_blank()

    # make status
    def make_start(self):
        if self.is_goal():
            return
        if Cell.start:
            Cell.start.make_blank()
        Cell.start = self

        self.color = Color.TURQUOISE

    def make_goal(self):
        if self.is_start():
            return

        if Cell.goal:
            Cell.goal.make_blank()
        Cell.goal = self

        self.color = Color.ORANGE

    def make_obstacle(self):
        if self.is_goal() or self.is_start():
            return
        self.color = Color.BLACK

    def make_blank(self):
        if self.is_start():
            Cell.start = None
        elif self.is_goal():
            Cell.goal = None

        self.color = Color.WHITE

    # A* algorithm
    def make_closed(self):
        self.color = Color.RED

    def make_open(self):
        self.color = Color.GREEN

    def make_path(self):
        self.color = Color.YELLOW

    # find all neighbors
    def update_neighbors(self, grid, size):
        n = []

        if self.row - 1 >= 0:
            cell = grid[self.row-1][self.col]
            if not cell.is_obstacle():
                n.append(cell)
        if self.row + 1 < size:
            cell = grid[self.row+1][self.col]
            if not cell.is_obstacle():
                n.append(cell)
        if self.col - 1 >= 0:
            cell = grid[self.row][self.col-1]
            if not cell.is_obstacle():
                n.append(cell)
        if self.col + 1 < size:
            cell = grid[self.row][self.col+1]
            if not cell.is_obstacle():
                n.append(cell)

        self.neighbors = n
        # return n

    # check status
    def is_start(self):
        return self.color == Color.TURQUOISE

    def is_goal(self):
        return self.color == Color.ORANGE

    def is_obstacle(self):
        return self.color == Color.BLACK

    def is_closed(self):
        self.color == Color.RED

    def is_open(self):
        self.Color == Color.GREEN
