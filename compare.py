from grid import Grid

from btree import BinaryTree
from sidewinder import Sidewinder
from aldous_brouder import AldousBroder
from wilson import Wilson
from hunt_kill import HuntAndKill

algos = [ BinaryTree, Sidewinder, AldousBroder, Wilson, HuntAndKill ]

tries = 100
size = 20
avgs = {}

for algo in algos:
    name = algo.__name__
    print("running {}".format(name))

    counts = []

    for i in range(tries):
        grid = Grid(size, size)
        algo.on(grid)
        counts.append(len(grid.dead_ends()))

    total = sum(counts)
    avgs[name] = total / len(counts)

    total_cells = size * size
    print("  Average dead-ends per {0}x{0} maze: {1}".format(size, avgs[name]))
