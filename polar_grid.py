from grid import Grid
from recursive_backtracker import RecursiveBacktracker
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

            # outer walls
            x1, x2 = center - outer_rad, center + outer_rad
            bounding_box = x1, x1, x2, x2

            ax = center + int(inner_rad * math.cos(theta_cw))
            ay = center + int(inner_rad * math.sin(theta_cw))
            bx = center + int(outer_rad * math.cos(theta_cw))
            by = center + int(outer_rad * math.sin(theta_cw))

            if cell.has_boundary_with(cell.north):
                deg_ccw = math.degrees(theta_cw)
                deg_cw = math.degrees(theta_ccw)
                color = '#0000ff' if cell.row == 0 else WALL_COLOR
                draw.arc([x1, x1, x2, x2], deg_cw, deg_ccw, color)

            if cell.has_boundary_with(cell.east):
                draw.line([ax, ay, bx, by], WALL_COLOR, WALL_PIXELS)

            # break

        img.save(name, 'PNG')

if  __name__ == '__main__':
    maze = PolarGrid(30, 30)
    RecursiveBacktracker.on(maze)

    maze.to_png(name='polar-arc.png')
