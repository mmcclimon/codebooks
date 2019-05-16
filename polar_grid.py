from grid import Grid
import math
from PIL import Image, ImageDraw

class PolarGrid(Grid):
    def to_png(self, name='maze.png'):
        OFFSET = 5
        CELL_SIZE = 10
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
            theta = 2 * math.pi / len(self.grid[ cell.row ])
            inner_rad = cell.row * CELL_SIZE
            outer_rad = (cell.row + 1) * CELL_SIZE
            theta_ccw = cell.col * theta
            theta_cw  = (cell.col + 1) * theta

            ax = center + int(inner_rad * math.cos(theta_ccw))
            ay = center + int(inner_rad * math.sin(theta_ccw))
            bx = center + int(outer_rad * math.cos(theta_ccw))
            by = center + int(outer_rad * math.sin(theta_ccw))

            cx = center + int(inner_rad * math.cos(theta_cw))
            cy = center + int(inner_rad * math.sin(theta_cw))
            dx = center + int(outer_rad * math.cos(theta_cw))
            dy = center + int(outer_rad * math.sin(theta_cw))

            if cell.has_boundary_with(cell.north):
                draw.line([ax, ay, cx, cy], WALL_COLOR, WALL_PIXELS)

            if cell.has_boundary_with(cell.east):
                draw.line([cx, cy, dx, dy], WALL_COLOR, WALL_PIXELS)

        img.save(name, 'PNG')

if  __name__ == '__main__':
    maze = PolarGrid(10, 10)
    maze.to_png(name='polar.png')
