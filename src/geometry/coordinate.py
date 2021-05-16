"""
I think the name gives it away
"""

import math
import operator
from collections import namedtuple
from functools import reduce


# do not instantiate directly. use with an iterable and it slaps some vector stuff on.
class Vector:
    """superclass for creating vectors with an arbitrary number of coordinates"""

    def __init__(self, *components):
        self.magnitude = math.hypot(*components)

    def _apply(self, operand, operation, scalars_allowed=True):
        """
        returns a vector with each component changed by a vector or scalar.
        also does basic type filtering.
        """

        if isinstance(operand, self.__class__):
            return True, self.__class__(
                *[operation(c_0, c_1) for c_0, c_1 in zip(self, operand)]
            )

        if scalars_allowed and isinstance(operand, (int, float)):
            # pylint: disable=E1133
            return True, self.__class__(*[operation(c, operand) for c in self])

        return False, None

    def __add__(self, operand):
        success, product = self._apply(operand, operator.add, False)
        if not success:
            raise ArithmeticError(f"Cannot add {type(operand)} to {type(self)}.")
        return product

    def __sub__(self, operand):
        success, product = self._apply(operand, operator.sub, False)
        if not success:
            raise ArithmeticError(f"Cannot subtract {type(operand)} from {type(self)}.")
        return product

    def __mul__(self, operand):
        success, product = self._apply(operand, operator.mul, True)
        if not success:
            raise ArithmeticError(f"Cannot multiply {type(self)} by {type(operand)}.")
        return product

    def __truediv__(self, operand):
        success, product = self._apply(operand, operator.truediv, True)
        if not success:
            raise ArithmeticError(f"Cannot divide {type(self)} by {type(operand)}.")
        return product

    def dot(self, operand):
        """calculates dot product of two vectors"""
        success, product = self._apply(operand, operator.mul, False)
        if not success:
            raise ArithmeticError(f"Cannot get dot product with {type(operand)}.")
        return reduce(lambda a, b: a + b, product)


# I am using namedtuples as iterables
class Vector2(Vector, namedtuple("CoordXY", ("x", "y"))):
    """a vector with x and y coordinates"""


# I made vector3 for fun because it isn't much different
# plus, what if we wanted to move turtle into the 3rd dimension?
class Vector3(Vector, namedtuple("CoordXYZ", ("x", "y", "z"))):
    """a vector with x y and z coordinates"""

    def cross(self, operand):
        """gets cross product of two vectors"""
        if not isinstance(operand, self.__class__):
            raise ArithmeticError(f"Cannot get cross product with {type(operand)}.")

        components = []
        for i in range(3):
            c_0 = (i + 1) % 3
            c_1 = (i + 2) % 3
            components.append(self[c_0] * operand[c_1] - self[c_1] * operand[c_0])

        return self.__class__(*components)
