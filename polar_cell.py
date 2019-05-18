from cell import Cell

class PolarCell(Cell):
    def __init__(self, grid, row, col):
        super().__init__(grid, row, col)
        self.cw      = None
        self.ccw     = None
        self.inward  = None
        self.outward = []

    def __repr__(self):
        return "<PolarCell[{},{}]>".format(
            self.row,
            self.col,
        )

    def neighbors(self):
        ret = list(filter(lambda c: c is not None, [ self.cw, self.ccw, self.inward ]))
        ret.extend(self.outward)
        return ret
