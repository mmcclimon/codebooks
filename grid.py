import random
import cell

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = self.prepare_grid()
        self.configure_cells()

    def __repr__(self):
        return repr(self.grid)

    def __str__(self):
        PIPE = '│'
        PLUS = '+'
        DASH = '───'

        dashplus = DASH + PLUS

        ret = PLUS + (dashplus * self.cols) + "\n"

        for row in self.each_row():
            top = PIPE
            bottom = PLUS

            for cell in row:
                body = '   '
                east_b = ' ' if cell.is_linked_to(cell.east) else PIPE
                top = top + body + east_b

                south_b = '   ' if cell.is_linked_to(cell.south) else DASH
                corner = PLUS
                bottom = bottom + south_b + corner

            ret = ret + top + '\n'
            ret = ret + bottom + '\n'

        return ret



    def prepare_grid(self):
        return [[cell.Cell(r, c) for c in range(self.cols)] for r in range(self.rows)]

    def get(self, row, col):
        if row < 0 or row > self.rows - 1:
            return None
        if col < 0 or col > self.cols - 1:
            return None
        return self.grid[row][col]

    def configure_cells(self):
        for cell in self.each_cell():
            row, col = cell.row, cell.col

            cell.north = self.get(row - 1, col)
            cell.south = self.get(row + 1, col)
            cell.west  = self.get(row, col - 1)
            cell.east  = self.get(row, col + 1)

    def random_cell(self):
        r = random.randint(self.rows - 1)
        c = random.randint(self.cols - 1)
        return self.get(r, c)

    def each_row(self):
        for row in self.grid:
            yield row

    def each_cell(self):
        for row in self.each_row():
            for cell in row:
                yield cell



if __name__ == '__main__':
    maze = Grid(5,5)
    print(maze)
