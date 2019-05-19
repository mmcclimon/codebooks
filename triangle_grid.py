from grid import Grid
from triangle_cell import TriangleCell
from recursive_backtracker import RecursiveBacktracker
from collections import namedtuple
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
        fields = ['offset', 'cell_size', 'bg_color', 'wall_color', 'wall_px']
        ImgData = namedtuple('ImgData', fields)
        img = ImgData(5, 25, '#ffffff', '#000000', 1)

        cell_height = img.cell_size * math.sqrt(3) / 2

        width = int(img.cell_size * (self.cols + 1) / 2) + img.offset * 2
        height = int(cell_height * self.rows) + img.offset * 2

        image_object = Image.new('RGB', (width, height), img.bg_color)
        draw = ImageDraw.Draw(image_object)

        if mode == 'color':
            self._generate_bg_colors()

        for method in [TriangleCell.draw_bg, TriangleCell.draw_walls]:
            for cell in self.each_cell():
                method(cell, draw, img)

        image_object.save(name, 'PNG')

if  __name__ == '__main__':
    maze = TriangleGrid(50, 75)
    RecursiveBacktracker.on(maze)
    maze.to_png(name='tri.png', mode='color')
