from grid import Grid
from polar_cell import PolarCell
from recursive_backtracker import RecursiveBacktracker
import random
import math
from PIL import Image, ImageDraw

class PolarGrid(Grid):
    def __init__(self, rows):
        super().__init__(rows, 1)


    def prepare_grid(self):
        row_height = 1 / self.rows

        rows = []
        rows.append([ PolarCell(0, 0) ])

        for idx in range(1, self.rows):
            radius = idx / self.rows
            circumference = 2 * math.pi * radius

            prev_count = len(rows[idx-1])
            est_width = circumference / prev_count
            ratio = round(est_width / row_height)
            num_cells = prev_count * ratio
            rows.append([PolarCell(self, idx, col) for col in range(num_cells)])

        return rows

    def configure_cells(self):
        for cell in self.each_cell():
            row, col = cell.row, cell.col

            if row > 0:
                cell.cw = self.get(row, col + 1)
                cell.ccw = self.get(row, col - 1)

                ratio = int(len(self.grid[row]) / len(self.grid[row-1]))
                parent = self.get(row - 1, int(col / ratio))
                parent.outward.append(cell)
                cell.inward = parent

    def get(self, row, col):
        if row < 0 or row > self.rows - 1:
            return None
        actual_col = col % len(self.grid[row])
        return self.grid[row][actual_col]

    def to_png(self, name='maze.png'):
        OFFSET = 5
        BG_COLOR = '#ffffff'
        WALL_COLOR = '#000000'
        WALL_PIXELS = 1
        CELL_SIZE = 15

        size = 2 * self.rows * CELL_SIZE
        center = (size // 2) + 5

        img = Image.new('RGB', (size+OFFSET*2,size+OFFSET*2), BG_COLOR)
        draw = ImageDraw.Draw(img)
        draw.ellipse([OFFSET, OFFSET, size+OFFSET, size+OFFSET], BG_COLOR, WALL_PIXELS)

        for cell in self.each_cell():
            if cell.row == 0:
                continue

            theta = 2 * math.pi / len(self.grid[ cell.row ])
            inner_rad = cell.row * CELL_SIZE
            outer_rad = (cell.row + 1) * CELL_SIZE
            theta_ccw = cell.col * theta
            theta_cw  = (cell.col + 1) * theta

            # outer walls
            x1, x2 = center - inner_rad, center + inner_rad
            bounding_box = x1, x1, x2, x2

            ax = center + int(inner_rad * math.cos(theta_cw))
            ay = center + int(inner_rad * math.sin(theta_cw))
            bx = center + int(outer_rad * math.cos(theta_cw))
            by = center + int(outer_rad * math.sin(theta_cw))

            if cell.has_boundary_with(cell.inward):
                deg_ccw = math.degrees(theta_cw)
                deg_cw = math.degrees(theta_ccw)
                draw.arc([x1, x1, x2, x2], deg_cw, deg_ccw, WALL_COLOR)

            if cell.has_boundary_with(cell.ccw):
                draw.line([ax, ay, bx, by], WALL_COLOR, WALL_PIXELS)

        img.save(name, 'PNG')

if  __name__ == '__main__':
    maze = PolarGrid(25)
    RecursiveBacktracker.on(maze)
    maze.to_png(name='polar-arc.png')
