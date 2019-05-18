from cell import Cell

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
