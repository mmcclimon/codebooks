from cell import Cell

# really, Cell should be more abstract and there should be a SquareCell that
# does most of the normal things. Alas.
class HexCell(Cell):
    def __init__(self, grid, row, col):
        super().__init__(grid, row, col)
        self.north = None
        self.south = None
        self.northeast = None
        self.northwest = None
        self.southeast = None
        self.southwest = None

    def neighbors(self):
        candidates = [ self.northwest, self.north, self.northeast,
                       self.southwest, self.south, self.southeast ]

        return list(filter(lambda c: c is not None, candidates))
