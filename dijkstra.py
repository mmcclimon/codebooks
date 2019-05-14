from grid import Grid
import sidewinder
import base36

class DistanceGrid(Grid):
    def __init__(self, rows, cols):
        self.distances = None
        super().__init__(rows, cols)

    def contents_of(self, cell):
        if cell in self.distances and self.distances[cell] is not None:
            return base36.dumps(self.distances[cell])
        return ' '


if __name__ == '__main__':
    grid = DistanceGrid(8,8)
    sidewinder.Sidewinder.on(grid)

    start = grid.get(0,0)
    distances = start.distances()
    new_start, dist = distances.max()

    new_distances = new_start.distances()
    goal, _ = new_distances.max()

    grid.distances = new_distances.path_to(goal)
    print(grid)
