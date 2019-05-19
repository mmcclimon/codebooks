from square_grid import SquareGrid
from btree import BinaryTree
from sidewinder import Sidewinder
from wilson import Wilson
from hunt_kill import HuntAndKill
import sys

if len(sys.argv) != 2:
    print("no filename given!")
    exit()

filename = sys.argv[1]

grid = SquareGrid(50,50)
Wilson.on(grid)
grid.to_png(name=filename, mode='path')
