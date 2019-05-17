class Distances:
    def __init__(self, root):
        self.root = root
        self.cells = {}
        self.cells[root] = 0
        self._max_dist = None
        self._max_cell = None

    def __repr__(self):
        return repr(self.cells)

    def __getitem__(self, k):
        try:
            return self.cells[k]
        except KeyError:
            return None

    def __setitem__(self, k, val):
        self.cells[k] = val

    def path_to(self, goal):
        current = goal

        breadcrumbs = Distances(self.root)
        breadcrumbs[current] = self.cells[current]

        while current != self.root:
            for neighbor in current.links:
                if self.cells[neighbor] < self.cells[current]:
                    breadcrumbs[neighbor] = self.cells[neighbor]
                    current = neighbor
                    break

        return breadcrumbs

    def max(self):
        if self._max_dist is not None:
            return (self._max_cell, self._max_dist)

        max_dist = 0
        max_cell = self.root

        for cell, dist in self.cells.items():
            if dist > max_dist:
                max_cell = cell
                max_dist = dist

        self._max_cell = max_cell
        self._max_dist = max_dist
        return (max_cell, max_dist)

    # NB unordered!
    def each_cell(self):
        for cell in self.cells.keys():
            yield cell
