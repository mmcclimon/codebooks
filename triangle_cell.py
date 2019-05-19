from cell import Cell
import math

class TriangleCell(Cell):
    def __init__(self, grid, row, col):
        super().__init__(grid, row, col)
        self.north = None
        self.south = None
        self.east = None
        self.west = None

    @property
    def is_upright(self):
        return (self.row + self.col) % 2 == 0

    def neighbors(self):
        candidates = [ self.east, self.west ]
        candidates.append(self.south if self.is_upright else self.north)
        return list(filter(lambda c: c is not None, candidates))

    def _coordinates_for(self, img):
        half_width = img.cell_size / 2
        height = img.cell_size * math.sqrt(3) / 2
        half_height = height / 2

        cx = img.offset + (half_width + self.col * half_width)
        cy = img.offset + (half_height + self.row * height)

        west_x = int(cx - half_width)
        mid_x = int(cx)
        east_x = int(cx + half_width)

        apex_y = int(cy - half_height)
        base_y = int(cy + half_height)

        if not self.is_upright:
            apex_y, base_y = base_y, apex_y

        # base_w, base_e, point
        return [(west_x, base_y), (east_x, base_y), (mid_x, apex_y)]

    def draw_bg(self, draw, img):
        color = self.grid.bg_color_for(self)
        if not color:
            return

        draw.polygon(self._coordinates_for(img), fill=color)

    def draw_walls(self, draw, img):
        base_w, base_e, point = self._coordinates_for(img)

        # always draw our eastern border
        if self.has_boundary_with(self.east):
            draw.line([base_e, point], img.wall_color, img.wall_px)

        # only draw west if there's nothing over there
        if not self.west:
            draw.line([base_w, point], img.wall_color, img.wall_px)

        # draw the base
        at_bottom = self.is_upright and not self.south
        has_north = self.has_boundary_with(self.north) and not self.is_upright

        if at_bottom or has_north:
            draw.line([base_w, base_e], img.wall_color, img.wall_px)
