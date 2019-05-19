from distances import Distances
import grid
import random

class Cell:
    def __init__(self, grid, row, col):
        self.grid = grid
        self.row = row
        self.col = col
        self.links = set()
        self.content = None
        self.bg_color = None

    def __repr__(self):
        return "<{}[{},{}]>".format(self.__class__, self.row, self.col)

    def key(self):
        return (self.__class__, self.row, self.col)

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
                    if linked not in distances:
                        distances[linked] = distances[cell] + 1
                        new_frontier.append(linked)

            frontier = new_frontier

        return distances
