from grid import Grid
import random

class AldousBroder:
    def on(grid):
        cell = grid.random_cell()
        unvisited = grid.size - 1
        seen = set()
        seen.add(cell)

        while len(seen) < grid.size:
            next_cell = cell.random_neighbor()
            if next_cell not in seen:
                cell.link(next_cell)
            seen.add(next_cell)
            cell = next_cell



if __name__ == '__main__':
    grid = Grid(10,10)
    AldousBroder.on(grid)
    print(grid.longest_path())
