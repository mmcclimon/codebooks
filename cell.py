from distances import Distances

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
        NORTH = 1
        EAST  = 2
        SOUTH = 4
        WEST  = 8
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
        n = NORTH if self.has_boundary_with(self.east)     else 0
        w = WEST  if self.has_boundary_with(self.south)    else 0
        e = EAST  if self.east.has_boundary_with(cell_se)  else 0
        s = SOUTH if self.south.has_boundary_with(cell_se) else 0

        wall_chars = {
            0     | 0     | 0     | 0     : ' ',
            0     | 0     | 0     | WEST  : '╴',
            0     | 0     | SOUTH | 0     : '╷',
            0     | 0     | SOUTH | WEST  : '┐',
            0     | EAST  | 0     | 0     : '╶',
            0     | EAST  | 0     | WEST  : '─',
            0     | EAST  | SOUTH | 0     : '┌',
            0     | EAST  | SOUTH | WEST  : '┬',
            NORTH | 0     | 0     | 0     : '╵',
            NORTH | 0     | 0     | WEST  : '┘',
            NORTH | 0     | SOUTH | 0     : '│',
            NORTH | 0     | SOUTH | WEST  : '┤',
            NORTH | EAST  | 0     | 0     : '└',
            NORTH | EAST  | 0     | WEST  : '┴',
            NORTH | EAST  | SOUTH | 0     : '├',
            NORTH | EAST  | SOUTH | WEST  : '┼',
        }

        return wall_chars[ n | e | s | w ]

    def sw_char(self):
        if self.col != 0:
            raise NotImplementedError('no use on non-initial columns')

        if self.row == self.grid.rows - 1:
            return '└'

        if self.has_boundary_with(self.south):
            return '├'

        return '│'
