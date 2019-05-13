class Cell:
    def __init__(self, grid, row, col):
        self.north = None
        self.east = None
        self.south = None
        self.west = None
        self.row = row
        self.col = col
        self.links = set()
        self.grid = grid    # XXX this is a cycle, but I don't care

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

    def has_boundary_with(self, cell):
        return not self.is_linked_to(cell)

    def neighbors(self):
        return filter(lambda cell: cell is not None, [self.north, self.east, self.south, self.west])

    # helpers for pretty-printing
    def ne_char(self):
        if self.row == 0 and self.col == self.grid.cols - 1:
            return '┐'

        if self.row == 0 and self.has_boundary_with(self.east):
            return '┬'

        if self.has_boundary_with(self.north) and self.has_boundary_with(self.east):
            return '┼'

        if self.has_boundary_with(self.east):
            return '┐'

        return '─'

    def se_char(self):
        last_col = self.grid.cols - 1

        # Bottom row.
        if self.row == self.grid.rows - 1:
            if self.col == last_col:
                return '┘'
            elif self.has_boundary_with(self.east):
                return '┴'
            else:
                return '─'

        # Right column.
        if self.col == last_col:
            if self.has_boundary_with(self.south):
                return '┤'
            else:
                return '│'

        # To actually know the character at the southeast of a cell, we need
        # to know both the south and east cells, but _also_ the southeast
        # cell. We'll build this character up tick by tick, I guess.
        cell_se = self.east.south
        n = self.has_boundary_with(self.east)
        w = self.has_boundary_with(self.south)
        e = self.east.has_boundary_with(cell_se)
        s = self.south.has_boundary_with(cell_se)

        # one prong
        if     n and not e and not s and not w: return '╵'
        if not n and     e and not s and not w: return '╶'
        if not n and not e and     s and not w: return '╷'
        if not n and not e and not s and     w: return '╴'

        # two prongs
        if     n and     e and not s and not w: return '└'
        if     n and not e and not s and     w: return '┘'
        if not n and     e and     s and not w: return '┌'
        if not n and not e and     s and     w: return '┐'
        if     n and not e and     s and not w: return '│'
        if not n and     e and not s and     e: return '─'

        # three prongs
        if n and e and w and not s: return '┴'
        if n and e and s and not w: return '├'
        if n and w and s and not e: return '┤'
        if s and e and w and not n: return '┬'

        # four prongs
        if n and e and s and w: return '┼'

        return 'x'

    def sw_char(self):
        if self.col != 0:
            raise NotImplementedError('no use on non-initial columns')

        if self.row == self.grid.rows - 1:
            return '└'

        if self.has_boundary_with(self.south):
            return '├'

        return '│'
