import random
from PIL import Image, ImageDraw

class Grid:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.distances = None
        self.grid = self.prepare_grid()
        self.configure_cells()

    def __repr__(self):
        return repr(self.grid)

    def prepare_grid(self):
        pass

    def configure_cells(self):
        pass

    def get(self, row, col):
        if row < 0 or row > self.rows - 1:
            return None
        if col < 0 or col > len(self.grid[row]) - 1:
            return None
        return self.grid[row][col]

    # from a cell's key()
    def get_by_key(self, key):
        _, row, col = key
        return self.get(row, col)

    def contents_of(self, cell):
        if cell.content:
            return cell.content

        if self.distances is None:
            return ' '

        if cell in self.distances and self.distances[cell] is not None:
            return self.int_to_char(self.distances[cell])
        return ' '

    def random_cell(self):
        row = random.choice(self.grid)
        return random.choice(row)

    def each_row(self):
        for row in self.grid:
            yield row

    def each_cell(self):
        for row in self.each_row():
            for cell in row:
                yield cell

    def dead_ends(self):
        return set(filter(lambda c: len(c.links) == 1, self.each_cell()))

    def _generate_bg_colors(self):
        start = self.get(self.rows//2, self.cols//2)
        self.distances = start.distances()

    def bg_color_for(self, cell):
        if cell.bg_color:
            return cell.bg_color

        if self.distances is None:
            return None

        if cell in self.distances and self.distances[cell] is not None:
            dist = self.distances[cell]
            _, maximum = self.distances.max()
            intensity = (maximum - dist) / maximum
            dark = int(255 * intensity)
            bright = int(128 + (127 * intensity))
            return "rgb({0},{1},{0})".format(dark, bright)


if __name__ == '__main__':
    maze = Grid(5,5)
    print(maze)
