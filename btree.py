from grid import Grid
import random

class BinaryTree:
    def on(grid):
        for cell in grid.each_cell():
            opts = list(filter(lambda c: c is not None, [ cell.north, cell.east]))

            if len(opts):
                cell.link(random.choice(opts))

if __name__ == '__main__':
    grid = Grid(10,10)
    BinaryTree.on(grid)
    print(grid)

