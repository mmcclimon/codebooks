from distances import Distances
import grid
import random

class Cell:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.links = set()
        self.content = None

    def __repr__(self):
        return "<Cell[{},{}]>".format(self.row, self.col)

    def _key(self):
        return (self.row, self.col)

    def __hash__(self):
        return hash(self._key())

    def __eq__(self, other):
        if other is None:
            return True

        return self._key() == other._key()

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

    def is_linked_to(self, other):
        return other in self.links

    def has_boundary_with(self, other):
        return not self.is_linked_to(other)

    def neighbors(self):
        pass

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
