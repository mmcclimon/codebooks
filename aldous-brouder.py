from grid import Grid
import random

class AldousBroder:
    def on(grid):
        cell = grid.random_cell()
        unvisited = grid.size - 1
        seen = set()
        seen.add(cell)

        while len(seen) < grid.size:
            next_cell = random.sample(list(cell.neighbors()), 1)[0]
            if next_cell not in seen:
                cell.link(next_cell)
            seen.add(next_cell)
            cell = next_cell



if __name__ == '__main__':
    grid = Grid(10,10)
    AldousBroder.on(grid)

    start = grid.get(0,0)
    distances = start.distances()
    new_start, dist = distances.max()

    new_distances = new_start.distances()
    goal, _ = new_distances.max()

    # grid.distances = new_distances.path_to(goal)
    new_start.content = 'S'
    goal.content = 'F'
    print(grid)
