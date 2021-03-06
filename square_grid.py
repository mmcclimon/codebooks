from grid import Grid
from square_cell import SquareCell
from PIL import Image, ImageDraw
from collections import namedtuple
import operator

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


class SquareGrid(Grid):
    def prepare_grid(self):
        return [[SquareCell(self, r, c) for c in range(self.cols)]
                for r in range(self.rows)]

    def configure_cells(self):
        for cell in self.each_cell():
            row, col = cell.row, cell.col

            cell.north = self.get(row - 1, col)
            cell.south = self.get(row + 1, col)
            cell.west  = self.get(row, col - 1)
            cell.east  = self.get(row, col + 1)

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

    def int_to_char(self, num):
        try:
            return ALPHABET[num]
        except IndexError:
            return '.'

    def to_png(self, name='maze.png', mode='blank', inset=0):
        fields = ['offset', 'cell_size', 'inset', 'bg_color', 'wall_color', 'wall_px']
        ImgData = namedtuple('ImgData', fields)

        cell_size = 16
        inset = cell_size * inset
        img = ImgData(5, cell_size, inset, '#ffffff', '#000000', 1)

        width = img.cell_size * self.cols + img.offset * 2
        height = img.cell_size * self.rows + img.offset * 2

        image_object = Image.new('RGB', (width, height), img.bg_color)
        draw = ImageDraw.Draw(image_object)

        if mode == 'path':
            self.longest_path()
            path = map(lambda t: t[0],
                    sorted(self.distances.items(), key=operator.itemgetter(1)))

        elif mode == 'color':
            self._generate_bg_colors()

        for method in [SquareCell.draw_bg, SquareCell.draw_walls]:
            for cell in self.each_cell():
                method(cell, draw, img)

        if mode == 'path':
            coords = [cell.center_for(img) for cell in path]
            draw.line(coords, '#77f0aa', 2)


        image_object.save(name, 'PNG')

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
            cell.bg_color = '#ffffff'

        new_start.content = 'S'
        new_start.bg_color = '#99cc99'
        goal.content = 'F'
        goal.bg_color = '#cc9999'
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
