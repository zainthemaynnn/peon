"""
it's like a turtle but cooler
"""

from turtle import Turtle
from geometry.coordinate import Vector2, lerp


class Peon(Turtle):
    """turtle class which draws along user input"""

    def __init__(self):
        super().__init__()
        self.penup()
        self.width(5)
        self.speed(0)

        self.canvas = self.getscreen()
        self.canvas.listen()

    # pylint: disable=C0103
    def tp(self, destination, rotation=0, speed=None):
        """releases pen, smoothly moves and rotates to position simultaneously"""
        was_down = self.isdown()
        self.pu()
        cur_speed = self.speed()
        if speed:
            self.speed(speed)

        base_pos, base_rot = self.pos(), self.heading()

        # approximately 1 step per 10 px
        steps = round((destination - base_pos).magnitude / 10)

        # find shortest rotation (leftwards or rightwards)
        if rotation > base_rot:
            if (diff := rotation - base_rot) > 180:
                diff -= 360
        else:
            if (diff := rotation - base_rot) < -180:
                diff += 360

        path = [
            (
                lerp(base_pos, destination, (delta := t / steps)),
                base_rot + diff * delta,
            )
            for t in range(1, steps + 1)
        ]

        for pos_data in path:
            coord, angle = pos_data
            self.goto(*coord)
            self.seth(angle)

        self.speed(cur_speed)
        if was_down:
            self.pd()

    def follow_path(self, path, reverse=False):
        """follows an array of coordinates"""
        if not reverse:
            if self.pos() != path[0]:
                self.tp(path[0], (path[1] - path[0]).angle)

            for coord in path[1:]:
                self.seth(self.towards(*coord))
                self.goto(coord)

        else:
            if self.pos() != path[-1]:
                self.tp(path[-1], (path[-2] - path[-1]).angle)

            for i in range(len(path) - 2, 0, -1):
                coord = path[i]
                self.seth(self.towards(*coord))
                self.goto(coord)

    def pos(self):
        """returns position vector"""
        return round(Vector2(*super().pos()))
