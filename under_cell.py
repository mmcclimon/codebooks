from square_cell import SquareCell

class UnderCell(SquareCell):
    def __init__(self, overcell):
        super().__init__(overcell.grid, overcell.row, overcell.col)

        if overcell.is_horizontal_passage:
            self.north = overcell.north
            overcell.north.south = self
            self.link(self.north)

            self.south = overcell.south
            overcell.south.north = self
            self.link(self.south)

        else:
            self.east = overcell.east
            overcell.east.west = self
            self.link(self.east)

            self.west = overcell.west
            overcell.west.east = self
            self.link(self.west)

    @property
    def is_horizontal_passage(self):
        return bool(self.east or self.west)

    @property
    def is_vertical_passage(self):
        return bool(self.north or self.south)

    def _draw_inset_walls(self, draw, img):
        x1, x2, x3, x4, y1, y2, y3, y4 = self._coordinates_for(img)

        if self.is_vertical_passage:
            draw.line([x2, y1, x2, y2], img.wall_color, img.wall_px)
            draw.line([x3, y1, x3, y2], img.wall_color, img.wall_px)
            draw.line([x2, y3, x2, y4], img.wall_color, img.wall_px)
            draw.line([x3, y3, x3, y4], img.wall_color, img.wall_px)
        else:
            draw.line([x1, y2, x2, y2], img.wall_color, img.wall_px)
            draw.line([x1, y3, x2, y3], img.wall_color, img.wall_px)
            draw.line([x3, y2, x4, y2], img.wall_color, img.wall_px)
            draw.line([x3, y3, x4, y3], img.wall_color, img.wall_px)
