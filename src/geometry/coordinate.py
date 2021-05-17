"""
along with many mathematical features of a vector
you can easily unpack them into components with *Vector
ok, so I learned turtle has its own vector2 and this is useless
it still has more stuff though so why not I guess
"""

import math
import operator
from collections import namedtuple
from functools import reduce


# do not instantiate directly. use with an iterable class and it slaps some vector stuff on.
class Vector:
    """superclass for creating vectors with an arbitrary number of coordinates"""

    # pylint: disable=E1133

    def _apply(self, operand, operation, errormsg=None, scalars_allowed=True):
        """
        returns a vector with each component changed by a vector or scalar.
        handles basic errors.
        """

        if isinstance(operand, self.__class__):
            return self.__class__(*[operation(c0, c1) for c0, c1 in zip(self, operand)])

        if scalars_allowed and isinstance(operand, (int, float)):
            return self.__class__(*[operation(c, operand) for c in self])

        raise TypeError(
            None if not errormsg else errormsg.format(type(self), type(operand))
        )

    def __add__(self, operand):
        return self._apply(operand, operator.add, "Cannot add to {} with {}.", False)

    # fmt: off
    def __sub__(self, operand):
        return self._apply(operand, operator.sub, "Cannot subtract from {} with {}.", False)
    # fmt: on

    def __mul__(self, operand):
        return self._apply(operand, operator.mul, "Cannot multiply {} by {}.", True)

    def __rmul__(self, operand):
        return self.__mul__(operand)

    def __truediv__(self, operand):
        return self._apply(operand, operator.truediv, "Cannot divide {} by {}.", True)

    def __floordiv__(self, operand):
        return self._apply(operand, operator.floordiv, "Cannot divide {} by {}.", True)

    def __abs__(self):
        return self.magnitude

    def __round__(self, precision=0):
        return self._apply(
            precision, round if precision != 0 else lambda a, b: int(round(a, b))
        )

    def __getattr__(self, key):
        if key == "magnitude":  # this is separate because calculating it is expensive
            setattr(self, "magnitude", math.hypot(*self))
            return self.magnitude
        raise AttributeError

    def dot(self, operand):
        """calculates dot product of two vectors"""
        return reduce(
            lambda a, b: a + b,
            self._apply(
                operand, operator.mul, "Cannot get dot product of {} with {}.", False
            ),
        )


# I am using namedtuples as iterables
class Vector2(Vector, namedtuple("CoordXY", ("x", "y"), defaults=[0, 0])):
    """a vector with x and y coordinates"""

    def rotate(self, n_deg):
        """returns vector rotated N degrees counterclockwise"""
        # https://matthew-brett.github.io/teaching/rotation_2d.html
        # pylint: disable=C0103
        rx, ry = self.x * n_deg, self.y * n_deg
        return self.__class__(math.cos(rx) - math.sin(ry), math.sin(rx) + math.cos(ry))


# I made vector3 for fun because it isn't much different
# plus, what if we wanted to move turtle into the 3rd dimension?
class Vector3(Vector, namedtuple("CoordXYZ", ("x", "y", "z"), defaults=[0, 0, 0])):
    """a vector with x y and z coordinates"""

    def cross(self, operand):
        """gets cross product of two vectors"""
        if not isinstance(operand, self.__class__):
            raise TypeError(f"Cannot get cross product with {type(operand)}.")

        # pylint: disable=C0103
        components = []
        for i in range(3):
            c0 = (i + 1) % 3
            c1 = (i + 2) % 3
            components.append(self[c0] * operand[c1] - self[c1] * operand[c0])

        return self.__class__(*components)
