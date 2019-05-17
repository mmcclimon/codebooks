from square_grid import SquareGrid
import random

class HuntAndKill:
    def on(grid):
        current = grid.random_cell()
        seen = set()

        while current:
            # Random walk
            neighbor = current.random_unvisited_neighbor()
            if neighbor:
                current.link(neighbor)
                current = neighbor
            else:
                current = None

                # hunt for unvisited cell next to a visited one
                for cell in grid.each_cell():
                    neighbor = cell.random_visited_neighbor()

                    if len(cell.links) == 0 and neighbor:
                        current = cell
                        current.link(neighbor)
                        break


if __name__ == '__main__':
    grid = SquareGrid(20,20)
    HuntAndKill.on(grid)
    print(grid.longest_path())
