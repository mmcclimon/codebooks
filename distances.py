class Distances:
    def __init__(self, root):
        self.root = root
        self._grid = root.grid
        self._max_dist = None
        self._max_cell = None

        # This is a terrible name, but I'm not sure what else to call it.
        # Inside this class, we'll key on cell.key(), but outside we'll
        # implement as getting/return cells.
        self._store = {}
        self._store[root.key()] = 0

    def __repr__(self):
        return repr(self._store)

    def __contains__(self, cell):
        return cell.key() in self._store

    def __getitem__(self, cell):
        try:
            return self._store[cell.key()]
        except KeyError:
            return None

    def __setitem__(self, cell, val):
        self._store[cell.key()] = val

    def path_to(self, goal):
        current = goal

        breadcrumbs = Distances(self.root)
        breadcrumbs[current] = self._store[current.key()]

        while current != self.root:
            ck = current.key()
            for neighbor in current.links:
                nk = neighbor.key()
                if self._store[nk] < self._store[ck]:
                    breadcrumbs[neighbor] = self._store[nk]
                    current = neighbor
                    break

        return breadcrumbs

    def max(self):
        if self._max_dist is not None:
            return (self._max_cell, self._max_dist)

        max_dist = 0
        max_key = self.root.key()

        for key, dist in self._store.items():
            if dist > max_dist:
                max_key = key
                max_dist = dist

        max_cell = self._grid.get_by_key(max_key)

        self._max_cell = max_cell
        self._max_dist = max_dist
        return (max_cell, max_dist)

    # NB unordered!
    def each_cell(self):
        for key in self._store.keys():
            yield self._grid.get_by_key(key)

    def items(self):
        for k, v in self._store.items():
            yield (self._grid.get_by_key(k), v)
