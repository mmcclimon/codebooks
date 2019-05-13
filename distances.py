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
