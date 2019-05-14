from grid import Grid
import random

class HuntAndKill:
    @classmethod
    def on(cls, grid):
        current = grid.random_cell()
        seen = set()

        while current:
            # Random walk
            neighbor = cls.pick_unvisited_neighbor(current)
            if neighbor:
                current.link(neighbor)
                current = neighbor
            else:
                current = None

                # hunt for unvisited cell next to a visited one
                for cell in grid.each_cell():
                    neighbor = cls.pick_visited_neighbor(cell)

                    if len(cell.links) == 0 and neighbor:
                        current = cell
                        current.link(neighbor)
                        break

    @classmethod
    def pick_unvisited_neighbor(cls, cell):
        return cls.pick_one(lambda c: len(c.links) == 0, cell)

    @classmethod
    def pick_visited_neighbor(cls, cell):
        return cls.pick_one(lambda c: len(c.links) > 0, cell)

    # returns a Maybe[cell]
    def pick_one(func, cell):
        xs = list(filter(func, cell.neighbors()))
        if len(xs) == 0:
            return None
        return random.sample(xs, 1)[0]

if __name__ == '__main__':
    grid = Grid(20,20)
    HuntAndKill.on(grid)
    print(grid.longest_path())
