class Distances:
    def __init__(self, root):
        self.root = root
        self.cells = {}
        self.cells[root] = 0

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
        max_dist = 0
        max_cell = self.root

        for cell, dist in self.cells.items():
            if dist > max_dist:
                max_cell = cell
                max_dist = dist

        return (max_cell, max_dist)

    # NB unordered!
    def each_cell(self):
        for cell in self.cells.keys():
            yield cell
