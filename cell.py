class Cell:
    # A cell should really have a weakref back to its parent, but I don't
    # really want to figure out weakrefs in python atm.
    def __init__(self, row, col):
        self.north = None
        self.east = None
        self.south = None
        self.west = None
        self.row = row
        self.col = col
        self.links = set()

    def __repr__(self):
        return "<Cell[{},{}], <{}{}{}{}>>".format(
            self.row,
            self.col,
            "n" if self.north else "-",
            "e" if self.east  else "-",
            "s" if self.south else "-",
            "w" if self.west  else "-",
        )

    def __key(self):
        return (self.row, self.col)

    def __hash__(self):
        return hash(self.__key())

    def __eq__(self, other):
        # This is daft, but I just want to do something so that I can use
        # cells as hash keys
        return self.__key() == other.__key()

    def __str__(self):
        if self.north and self.east and self.west and self.south:
            return "[]"
        return ""

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

    def neighbors(self):
        return filter(lambda cell: cell is not None, [self.north, self.east, self.south, self.west])

