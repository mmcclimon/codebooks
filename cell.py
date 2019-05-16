from distances import Distances
import grid
import random

class Cell:
    def __init__(self, row, col):
        self.north = None
        self.east = None
        self.south = None
        self.west = None
        self.row = row
        self.col = col
        self.links = set()
        self.content = None

    def __repr__(self):
        return "<Cell[{},{}], <{}{}{}{}>>".format(
            self.row,
            self.col,
            "n" if self.north else "-",
            "e" if self.east  else "-",
            "s" if self.south else "-",
            "w" if self.west  else "-",
        )

    def _key(self):
        return (self.row, self.col)

    def __hash__(self):
        return hash(self._key())

    def __eq__(self, other):
        if other is None:
            return True

        return self._key() == other._key()

    def __str__(self):
        if self.north and self.east and self.west and self.south:
            return "[]"
        return ""

    def distances(self):
        distances = Distances(self)
        frontier = [self]

        while len(frontier) > 0:
            new_frontier = []

            for cell in frontier:
                for linked in cell.links:
                    if linked not in distances.cells:
                        distances[linked] = distances[cell] + 1
                        new_frontier.append(linked)

            frontier = new_frontier

        return distances

    def link(self, other_cell, bidi=True):
        self.links.add(other_cell)
        if bidi:
            other_cell.link(self, False)
        return self

    def unlink(self, other_cell, bidi=True):
        self.links.discard(other_cell)
        if bidi:
            other_cell.unlink(self, False)
        return self

    def links(self):
        return self.links

    def is_linked_to(self, cell):
        return cell in self.links

    def has_boundary_with(self, cell):
        return not self.is_linked_to(cell)

    def neighbors(self):
        return filter(lambda cell: cell is not None, [self.north, self.east, self.south, self.west])

    def _pick_one(self, func):
        xs = list(filter(func, self.neighbors()))
        if len(xs) == 0:
            return None
        return random.sample(xs, 1)[0]

    def random_neighbor(self):
        return self._pick_one(lambda c: True)

    def random_unvisited_neighbor(self):
        return self._pick_one(lambda c: len(c.links) == 0)

    def random_visited_neighbor(self):
        return self._pick_one(lambda c: len(c.links) > 0)


    # helpers for pretty-printing
    def ne_char(self):
        cell_ne = self.north.east if self.north else None

        n = self.north and self.north.has_boundary_with(cell_ne)
        e = self.east  and self.east.has_boundary_with(cell_ne)
        s = self.has_boundary_with(self.east)
        w = self.has_boundary_with(self.north)

        return self.intersection_char(n, e, s, w)


    def se_char(self):
        # To actually know the character at the southeast of a cell, we need
        # to know both the south and east cells, but _also_ the southeast
        # cell. We'll build this character up tick by tick, I guess.
        cell_se = self.east.south if self.east else None

        n = self.has_boundary_with(self.east)
        e = self.east  and self.east.has_boundary_with(cell_se)
        s = self.south and self.south.has_boundary_with(cell_se)
        w = self.has_boundary_with(self.south)

        return self.intersection_char(n, e, s, w)

    def sw_char(self):
        cell_sw = self.south.west if self.south else None

        n = self.has_boundary_with(self.west)
        e = self.has_boundary_with(self.south)
        s = self.south and self.south.has_boundary_with(cell_sw)
        w = self.west  and self.west.has_boundary_with(cell_sw)

        return self.intersection_char(n, e, s, w)

    def intersection_char(self, n, e, s, w):
        n = grid.NORTH if n else 0
        e = grid.EAST  if e else 0
        s = grid.SOUTH if s else 0
        w = grid.WEST  if w else 0

        return grid.WALL_CHARS[ n | e | s | w ]
