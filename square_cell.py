from cell import Cell
import square_grid as grid

class SquareCell(Cell):
    def __init__(self, row, col):
        super().__init__(row, col)
        self.north = None
        self.east = None
        self.south = None
        self.west = None

    def neighbors(self):
        return filter(lambda cell: cell is not None, [self.north, self.east, self.south, self.west])

    # helpers for pretty-printing
    def ne_char(self):
        cell_ne = self.north.east if self.north else None

        n = self.north and self.north.has_boundary_with(cell_ne)
        e = self.east  and self.east.has_boundary_with(cell_ne)
        s = self.has_boundary_with(self.east)
        w = self.has_boundary_with(self.north)

        return self.intersection_char(n, e, s, w)


    def se_char(self):
        # To actually know the character at the southeast of a cell, we need
        # to know both the south and east cells, but _also_ the southeast
        # cell. We'll build this character up tick by tick, I guess.
        cell_se = self.east.south if self.east else None

        n = self.has_boundary_with(self.east)
        e = self.east  and self.east.has_boundary_with(cell_se)
        s = self.south and self.south.has_boundary_with(cell_se)
        w = self.has_boundary_with(self.south)

        return self.intersection_char(n, e, s, w)

    def sw_char(self):
        cell_sw = self.south.west if self.south else None

        n = self.has_boundary_with(self.west)
        e = self.has_boundary_with(self.south)
        s = self.south and self.south.has_boundary_with(cell_sw)
        w = self.west  and self.west.has_boundary_with(cell_sw)

        return self.intersection_char(n, e, s, w)

    def intersection_char(self, n, e, s, w):
        n = grid.NORTH if n else 0
        e = grid.EAST  if e else 0
        s = grid.SOUTH if s else 0
        w = grid.WEST  if w else 0

        return grid.WALL_CHARS[ n | e | s | w ]
