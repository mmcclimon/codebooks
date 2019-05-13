from grid import Grid
import btree
import base36

class DistanceGrid(Grid):
    def __init__(self, rows, cols):
        self.distances = None
        super().__init__(rows, cols)

    def contents_of(self, cell):
        if cell in self.distances:
            return base36.dumps(self.distances[cell])
        return ' '


if __name__ == '__main__':
    grid = DistanceGrid(5,5)
    btree.BinaryTree.on(grid)

    start = grid.get(0,0)
    distances = start.distances()

    grid.distances = distances
    print(grid)
