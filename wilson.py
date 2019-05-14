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
    grid = Grid(20,20)
    Wilson.on(grid)
    print(grid.longest_path())
