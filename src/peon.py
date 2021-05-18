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
        self.speed(10)

        self.canvas = self.getscreen()
        self.canvas.listen()

    def tp(self, destination, rotation, steps=20, speed=None):  # pylint: disable=C0103
        """releases pen, smoothly moves and rotates to position simultaneously"""
        self.pu()
        cur_speed = self.speed()
        if speed:
            self.speed(speed)

        base_pos, base_rot = self.pos(), self.heading()
        print(base_rot, rotation)
        if base_rot - rotation < -180:
            rotation = rotation - 360

        path = [
            (
                lerp(base_pos, destination, (delta := t / steps)),
                lerp(base_rot, rotation, delta),
            )
            for t in range(1, steps + 1)
        ]

        for pos_data in path:
            coord, angle = pos_data
            self.goto(*coord)
            self.seth(angle)

        self.speed(cur_speed)
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
