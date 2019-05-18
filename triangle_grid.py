from grid import Grid
from triangle_cell import TriangleCell
from recursive_backtracker import RecursiveBacktracker
import math
import random
from PIL import Image, ImageDraw

class TriangleGrid(Grid):
    def prepare_grid(self):
        return [[TriangleCell(self, r, c) for c in range(self.cols)]
                for r in range(self.rows)]

    def configure_cells(self):
        for cell in self.each_cell():
            row, col = cell.row, cell.col

            cell.west  = self.get(row, col - 1)
            cell.east  = self.get(row, col + 1)

            if cell.is_upright:
                cell.south = self.get(row + 1, col)
            else:
                cell.north = self.get(row - 1, col)


    def to_png(self, name='maze.png', mode='blank'):
        OFFSET = 5
        BG_COLOR = '#ffffff'
        WALL_COLOR = '#000000'
        WALL_PIXELS = 1
        CELL_SIZE = 25

        width = CELL_SIZE
        half_width = width / 2
        height = CELL_SIZE * math.sqrt(3) / 2
        half_height = height / 2

        img_width = int(CELL_SIZE * (self.cols + 1) / 2) + OFFSET*2
        img_height = int(height * self.rows) + OFFSET*2

        img = Image.new('RGB', (img_width+1,img_height+1), BG_COLOR)
        draw = ImageDraw.Draw(img)

        def coords_for_cell(cell):
            cx = OFFSET + (half_width + cell.col * half_width)
            cy = OFFSET + (half_height + cell.row * height)

            west_x = int(cx - half_width)
            mid_x = int(cx)
            east_x = int(cx + half_width)

            apex_y = int(cy - half_height)
            base_y = int(cy + half_height)

            if not cell.is_upright:
                apex_y, base_y = base_y, apex_y

            return (west_x, mid_x, east_x, apex_y, base_y) # gross

        if mode == 'color':
            start = self.get(self.rows//2, self.cols//2)
            self.distances = start.distances()

            # draw backgrounds first, because the lines need to overdraw
            for cell in self.each_cell():
                color = self.bg_color_for(cell)
                if color:
                    west_x, mid_x, east_x, apex_y, base_y = coords_for_cell(cell)
                    points = [(west_x, base_y), (mid_x, apex_y), (east_x, base_y)]
                    draw.polygon(points, fill=color)

        for cell in self.each_cell():
            west_x, mid_x, east_x, apex_y, base_y = coords_for_cell(cell)

            if not cell.west:
                draw.line([west_x, base_y, mid_x, apex_y], WALL_COLOR, WALL_PIXELS)

            if cell.has_boundary_with(cell.east):
                draw.line([east_x, base_y, mid_x, apex_y], WALL_COLOR, WALL_PIXELS)

            no_south = cell.is_upright and not cell.south
            unlinked = not cell.is_upright and cell.has_boundary_with(cell.north)

            if no_south or unlinked:
                draw.line([west_x, base_y, east_x, base_y], WALL_COLOR, WALL_PIXELS)


        img.save(name, 'PNG')

if  __name__ == '__main__':
    maze = TriangleGrid(50, 75)
    RecursiveBacktracker.on(maze)
    maze.to_png(name='tri.png', mode='color')
