from grid import Grid
import random

class BinaryTree:
    def on(grid):
        for cell in grid.each_cell():
            neighbors = set()
            if cell.north:
                neighbors.add(cell.north)
            if cell.east:
                neighbors.add(cell.east)

            if len(neighbors) > 0:
                n = random.sample(neighbors, 1)[0]
                cell.link(n)

if __name__ == '__main__':
    grid = Grid(10,10)
    BinaryTree.on(grid)
    print(grid)

