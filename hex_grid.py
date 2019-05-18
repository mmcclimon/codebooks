from grid import Grid
from hex_cell import HexCell
from recursive_backtracker import RecursiveBacktracker
import math
import random
from PIL import Image, ImageDraw

class HexGrid(Grid):
    def prepare_grid(self):
        return [[HexCell(self, r, c) for c in range(self.cols)]
                for r in range(self.rows)]

    def configure_cells(self):
        for cell in self.each_cell():
            row, col = cell.row, cell.col

            north_diag = row - 1 if col % 2 == 0 else row
            south_diag = row     if col % 2 == 0 else row + 1

            cell.northwest = self.get(north_diag, col - 1)
            cell.north     = self.get(row - 1, col)
            cell.northeast = self.get(north_diag, col + 1)
            cell.southwest = self.get(south_diag, col - 1)
            cell.south     = self.get(row + 1, col)
            cell.southeast = self.get(south_diag, col + 1)

    def to_png(self, name='maze.png', mode='blank'):
        # OFFSET = 5
        BG_COLOR = '#ffffff'
        WALL_COLOR = '#000000'
        WALL_PIXELS = 1
        CELL_SIZE = 15

        # this is all extremely copypasta, but I will make some effort at
        # understanding it a bit later.
        a_size = CELL_SIZE / 2
        b_size = CELL_SIZE * math.sqrt(3) / 2
        width  = CELL_SIZE * 2
        height = b_size * 2

        img_width = int(3 * a_size * self.cols + a_size + 0.5)
        img_height = int(height * self.rows + b_size + 0.5)

        img = Image.new('RGB', (img_width+1,img_height+1), BG_COLOR)
        draw = ImageDraw.Draw(img)

        def coords_for_cell(cell):
            cx = CELL_SIZE + 3 * cell.col * a_size
            cy = b_size + cell.row * height
            if cell.col % 2 == 1:
                cy += b_size

            # f/n = far/near, n/s/e/w = north/south/east/west
            xfw = int(cx - CELL_SIZE)
            xnw = int(cx - a_size)
            xne = int(cx + a_size)
            xfe = int(cx + CELL_SIZE)

            # c = center
            yn = int(cy - b_size)
            yc = int(cy)
            ys = int(cy + b_size)

            return (xfw, xnw, xne, xfe, yn, yc, ys)     # gross

        if mode == 'color':
            start = self.get(self.rows//2, self.cols//2)
            self.distances = start.distances()

            # draw backgrounds first, because the lines need to overdraw
            for cell in self.each_cell():
                color = self.bg_color_for(cell)
                if color:
                    xfw, xnw, xne, xfe, yn, yc, ys = coords_for_cell(cell)
                    points = [(xfw, yc), (xnw, yn), (xne, yn),
                              (xfe, yc), (xne, ys), (xnw, ys)]
                    draw.polygon(points, fill=color)

        for cell in self.each_cell():
            xfw, xnw, xne, xfe, yn, yc, ys = coords_for_cell(cell)

            if not cell.southwest:
                draw.line([xfw, yc, xnw, ys], WALL_COLOR, WALL_PIXELS)
            if not cell.northwest:
                draw.line([xfw, yc, xnw, yn], WALL_COLOR, WALL_PIXELS)
            if not cell.north:
                draw.line([xnw, yn, xne, yn], WALL_COLOR, WALL_PIXELS)

            if cell.has_boundary_with(cell.northeast):
                draw.line([xne, yn, xfe, yc], WALL_COLOR, WALL_PIXELS)
            if cell.has_boundary_with(cell.southeast):
                draw.line([xfe, yc, xne, ys], WALL_COLOR, WALL_PIXELS)
            if cell.has_boundary_with(cell.south):
                draw.line([xne, ys, xnw, ys], WALL_COLOR, WALL_PIXELS)

        img.save(name, 'PNG')

if  __name__ == '__main__':
    maze = HexGrid(35, 35)
    RecursiveBacktracker.on(maze)
    maze.to_png(name='hex.png', mode='color')
