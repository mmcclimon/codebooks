from grid import Grid
import random

class Wilson:
    def on(grid):
        unvisited = set(grid.each_cell())

        first = random.sample(unvisited, 1)[0]
        unvisited.remove(first)

        while len(unvisited) > 0:
            cell = random.sample(unvisited, 1)[0]
            path = [ cell ]

            while cell in unvisited:
                cell = random.sample(list(cell.neighbors()), 1)[0]
                try:
                    pos = path.index(cell)
                    path = path[0:pos+1]
                except ValueError:
                    path.append(cell)

            for idx in range(len(path)-1):
                path[idx].link(path[idx+1])
                unvisited.remove(path[idx])


if __name__ == '__main__':
    grid = Grid(10,10)
    Wilson.on(grid)

    start = grid.get(0,0)
    distances = start.distances()
    new_start, dist = distances.max()

    new_distances = new_start.distances()
    goal, _ = new_distances.max()

    new_start.content = 'S'
    goal.content = 'F'
    print(grid)
