from grid import Grid
from square_cell import SquareCell
from PIL import Image, ImageDraw

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
        return [[SquareCell(r, c) for c in range(self.cols)] for r in range(self.rows)]

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

    def to_png(self, name='maze.png', mode='blank'):
        OFFSET = 5  # so the walls aren't at the edge of the image
        BG_COLOR = '#ffffff'
        WALL_COLOR = '#000000'
        WALL_PIXELS = 1
        CELL_SIZE = 15

        width = CELL_SIZE * self.cols
        height = CELL_SIZE * self.rows

        img = Image.new('RGB', (width+OFFSET*2,height+OFFSET*2), BG_COLOR)
        draw = ImageDraw.Draw(img)

        def coords_for_cell(cell):
            w = OFFSET + cell.col * CELL_SIZE
            n = OFFSET + cell.row * CELL_SIZE
            e = OFFSET + (cell.col + 1) * CELL_SIZE
            s = OFFSET + (cell.row + 1) * CELL_SIZE
            return (w, n, e, s)

        if mode == 'color':
            start = self.get(self.rows//2, self.cols//2)
            self.distances = start.distances()

            # draw backgrounds first, because the lines need to overdraw
            for cell in self.each_cell():
                color = self.bg_color_for(cell)
                if color:
                    w,n,e,s = coords_for_cell(cell)
                    draw.rectangle([w, n, e, s], fill=color)

        for cell in self.each_cell():
            w,n,e,s = coords_for_cell(cell)

            # Every cell draws its own eastern/southern borders
            if cell.has_boundary_with(cell.east):
                draw.line([e, n, e, s], WALL_COLOR, WALL_PIXELS)

            if cell.has_boundary_with(cell.south):
                draw.line([w, s, e, s], WALL_COLOR, WALL_PIXELS)

            # But if there are no cells to the north or west, it should draw
            # that border too.
            if not cell.north:
                draw.line([w, n, e, n], WALL_COLOR, WALL_PIXELS)
            if not cell.west:
                draw.line([w, n, w, s], WALL_COLOR, WALL_PIXELS)

        img.save(name, 'PNG')

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
