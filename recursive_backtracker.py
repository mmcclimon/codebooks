from grid import Grid
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
    grid = Grid(20,20)
    RecursiveBacktracker.on(grid)
    print(grid.longest_path())
    print("dead ends = {}".format(len(grid.dead_ends())))
