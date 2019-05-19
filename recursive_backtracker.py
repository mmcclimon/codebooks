from square_grid import SquareGrid
from weave_grid import WeaveGrid
import random

class RecursiveBacktracker:
    def on(grid):
        stack = []
        current = grid.random_cell()
        stack.append(current)

        while len(stack):
            current = stack[-1]
            n = current.random_unvisited_neighbor()

            if n:
                current.link(n)
                stack.append(n)
            else:
                # no unvisited neighbors
                stack.pop()


if __name__ == '__main__':
    grid = WeaveGrid(35,35)
    RecursiveBacktracker.on(grid)
    grid.to_png(name='woven.png', inset=0.1)
