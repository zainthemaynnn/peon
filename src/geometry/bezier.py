"""
tools for creating bezier curves
"""

from bisect import bisect_left
from math import comb
from .coordinate import lerp


class Bezier:
    """creates a bezier using N points"""

    def __init__(self, *coords):
        self.root_points = coords
        self.order = len(self.root_points) - 1

    def map(self, n_points):
        """returns bezier coordinates"""
        coords = [self.root_points[0]]
        for step in range(1, n_points):
            coords.append(self.get_coord(step / (n_points - 1)))
        return coords

    def map_eq(self, n_points):
        """returns bezier coordinates, spaced equally"""
        # see: https://gamedev.stackexchange.com/a/5427

        coords = [self.root_points[0]]  # final coords
        arc_lengths = [0]  # arc length at a specific coord (separated for bisect)
        unshifted = [
            (coords[0], arc_lengths[0])  # tuples of: (coord, arc length to next coord)
        ]
        arc_total = 0  # total length of bezier

        prev_coord = self.root_points[0]

        for step in range(1, n_points):
            coord = self.get_coord(step / (n_points - 1))
            distance = (coord - prev_coord).magnitude
            arc_total += distance
            unshifted.append((coord, distance))
            arc_lengths.append(arc_total)
            prev_coord = coord

        for step in range(1, n_points):
            target = arc_total * (step / (n_points - 1))
            i = bisect_left(arc_lengths, target)

            nearest = arc_lengths[i]
            coord, distance = unshifted[i]
            prev_coord = unshifted[i - 1][0]

            coords.append(round(lerp(coord, prev_coord, (nearest - target) / distance)))

        return coords

    def get_coord(self, t):
        """returns a single coordinate (unspaced) along the curve from delta 0-1"""
        # a bezier of order N is just (t + (1 - t)) ^ N
        # with each product multiplied by the respective point
        # pylint: disable=C0103
        s = 1 - t
        product = self.root_points[0].__class__()  # initialize empty vector
        for i, coord in enumerate(self.root_points):
            product += coord * (comb(self.order, i) * t ** i * s ** (self.order - i))
        return round(product)
