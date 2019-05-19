from square_cell import SquareCell

class OverCell(SquareCell):
    def neighbors(self):
        ret = list(super().neighbors())
        if self.can_tunnel_north():
            ret.append(self.north.north)
        if self.can_tunnel_south():
            ret.append(self.south.south)
        if self.can_tunnel_east():
            ret.append(self.east.east)
        if self.can_tunnel_west():
            ret.append(self.west.west)

        return ret

    def can_tunnel_north(self):
        return self.north and self.north.north and self.north.is_horizontal_passage

    def can_tunnel_south(self):
        return self.south and self.south.south and self.south.is_horizontal_passage

    def can_tunnel_east(self):
        return self.east and self.east.east and self.east.is_vertical_passage

    def can_tunnel_west(self):
        return self.west and self.west.west and self.west.is_vertical_passage

    @property
    def is_horizontal_passage(self):
        return (self.is_linked_to(self.east) and self.is_linked_to(self.west) and
                self.has_boundary_with(self.north) and self.has_boundary_with(self.south))

    @property
    def is_vertical_passage(self):
        return (self.is_linked_to(self.north) and self.is_linked_to(self.south) and
                self.has_boundary_with(self.east) and self.has_boundary_with(self.west))

    def link(self, other_cell, bidi=True):
        neighbor = None

        if self.north and self.north == other_cell.south:
            neighbor = self.north
        elif self.south and self.south == other_cell.north:
            neighbor = self.south
        elif self.east and self.east == other_cell.west:
            neighbor = self.east
        elif self.west and self.west == other_cell.east:
            neighbor = self.west

        if neighbor:
            self.grid.tunnel_under(neighbor)
        else:
            super().link(other_cell, bidi)
