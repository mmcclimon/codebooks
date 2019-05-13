from grid import Grid
import random

class Sidewinder:
    def on(grid):
        for row in grid.each_row():
            run = set()

            for cell in row:
                run.add(cell)

                at_east = cell.east is None
                at_north = cell.north is None

                should_close = at_east or (
                        not at_north and random.choice([True, False]))

                if should_close:
                    mem = random.sample(run, 1)[0]
                    if(mem.north):
                        mem.link(mem.north)
                    run.clear()
                else:
                    cell.link(cell.east)



if __name__ == '__main__':
    grid = Grid(10,10)
    Sidewinder.on(grid)
    print(grid)

