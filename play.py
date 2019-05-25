from square_grid import SquareGrid
from hex_grid import HexGrid
from triangle_grid import TriangleGrid
from polar_grid import PolarGrid
from weave_grid import WeaveGrid
from btree import BinaryTree
from sidewinder import Sidewinder
from wilson import Wilson
from hunt_kill import HuntAndKill
from recursive_backtracker import RecursiveBacktracker
import sys

if len(sys.argv) != 2:
    print("no filename given!")
    exit()

filename = sys.argv[1]

grid = WeaveGrid(30, 30)
RecursiveBacktracker.on(grid)
grid.to_png(name=filename, inset=0.1)
