import random
import base36
import cell

ALPHABET = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
NORTH = 1
EAST  = 2
SOUTH = 4
WEST  = 8
WALL_CHARS = {
    0     | 0     | 0     | 0     : ' ',
    0     | 0     | 0     | WEST  : '╴',
    0     | 0     | SOUTH | 0     : '╷',
    0     | 0     | SOUTH | WEST  : '┐',
    0     | EAST  | 0     | 0     : '╶',
    0     | EAST  | 0     | WEST  : '─',
    0     | EAST  | SOUTH | 0     : '┌',
    0     | EAST  | SOUTH | WEST  : '┬',
    NORTH | 0     | 0     | 0     : '╵',
    NORTH | 0     | 0     | WEST  : '┘',
    NORTH | 0     | SOUTH | 0     : '│',
    NORTH | 0     | SOUTH | WEST  : '┤',
    NORTH | EAST  | 0     | 0     : '└',
    NORTH | EAST  | 0     | WEST  : '┴',
    NORTH | EAST  | SOUTH | 0     : '├',
    NORTH | EAST  | SOUTH | WEST  : '┼',
}

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.size = rows * cols
        self.grid = self.prepare_grid()
        self.distances = None
        self.configure_cells()

    def __repr__(self):
        return repr(self.grid)

    # We draw top-left to bottom-right, so in general, we only need to know
    # the southeast character. But we need to know northeast characters for
    # the top row and southwest characters for the left column. Those are
    # implemented (badly) as methods on cells.
    def __str__(self):
        PIPE = '│'
        DASH = '───'

        ret = WALL_CHARS[ SOUTH | EAST ] #  gotta start somewhere.

        # do top border
        for cell in self.grid[0]:
            ret += DASH + cell.ne_char()
        ret += '\n'

        for row in self.each_row():
            mid = PIPE
            bottom = row[0].sw_char()

            for cell in row:
                body = ' {} '.format(self.contents_of(cell))
                east_b = ' ' if cell.is_linked_to(cell.east) else PIPE
                mid += body + east_b

                south_b = '   ' if cell.is_linked_to(cell.south) else DASH
                bottom += south_b + cell.se_char()

            ret += mid + '\n'
            ret += bottom + '\n'

        return ret


    def prepare_grid(self):
        return [[cell.Cell(self, r, c) for c in range(self.cols)] for r in range(self.rows)]

    def get(self, row, col):
        if row < 0 or row > self.rows - 1:
            return None
        if col < 0 or col > self.cols - 1:
            return None
        return self.grid[row][col]

    def contents_of(self, cell):
        if cell.content:
            return cell.content

        if self.distances is None:
            return ' '

        if cell in self.distances and self.distances[cell] is not None:
            return self.int_to_char(self.distances[cell])
        return ' '

    def configure_cells(self):
        for cell in self.each_cell():
            row, col = cell.row, cell.col

            cell.north = self.get(row - 1, col)
            cell.south = self.get(row + 1, col)
            cell.west  = self.get(row, col - 1)
            cell.east  = self.get(row, col + 1)

    def random_cell(self):
        r = random.randint(0, self.rows - 1)
        c = random.randint(0, self.cols - 1)
        return self.get(r, c)

    def each_row(self):
        for row in self.grid:
            yield row

    def each_cell(self):
        for row in self.each_row():
            for cell in row:
                yield cell

    def int_to_char(self, num):
        try:
            return ALPHABET[num]
        except IndexError:
            return '.'

    # these methods for printing all mutate state, which I'm not crazy about,
    # but they're also convenient for now.
    def longest_path(self):
        # this prints S and F with dots for the path
        start = self.get(0,0)
        distances = start.distances()
        new_start, dist = distances.max()

        new_distances = new_start.distances()
        goal, _ = new_distances.max()
        self.distances = new_distances.path_to(goal)

        for cell in self.distances.each_cell():
            cell.content = '•'

        new_start.content = 'S'
        goal.content = 'F'
        return str(self)

    def start_finish(self):
        start = self.get(0,0)
        distances = start.distances()
        new_start, dist = distances.max()

        new_distances = new_start.distances()
        goal, _ = new_distances.max()
        self.distances = None

        new_start.content = 'S'
        goal.content = 'F'
        return str(self)

    def blank(self):
        self.distances = None
        for cell in self.each_cell():
            cell.content = None

        return str(self)


if __name__ == '__main__':
    maze = Grid(5,5)
    print(maze)
