from square_grid import SquareGrid
from over_cell   import OverCell
from under_cell  import UnderCell
from warnings import warn

class WeaveGrid(SquareGrid):
    def __init__(self, rows, cols):
        self.undercells = []
        super().__init__(rows, cols)

    def prepare_grid(self):
        return [[OverCell(self, r, c) for c in range(self.cols)]
                for r in range(self.rows)]

    def tunnel_under(self, overcell):
        uc = UnderCell(overcell)
        self.undercells.append(uc)

    def each_cell(self):
        yield from super().each_cell()
        for cell in self.undercells:
            yield cell


