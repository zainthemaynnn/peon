"""
this is where the drawing takes place
compared to the rest, this is pretty rushed and therefore long
just because of the sheer tediousness of mapping everything properly
"""

import turtle
import math
from peon import Peon
from geometry.coordinate import Vector2, lerp
from geometry.bezier import Bezier

constants = {
    "center": Vector2(0, -100),
    "radius": 150,
    "torso": {
        "stomach_arch": Vector2(0, 20),
        "shadow": 120,
        "shadow_dip": Vector2(0, -100),
    },
    "legs": {"principal": 60},
    "details": {
        "buttons": [Vector2(-60, -15), Vector2(60, -15)],
        "yellow_thingies": [Vector2(-50, 30), Vector2(50, 30)],
    },
    "face": {
        "radius": 50,
        "smile_inset": 10,
        "glasses": [Vector2(-15, 15), Vector2(15, 15)],
        "moustache_length": 80,
        "teeth": 6,
    },
}

peon = Peon()


def mirror(vec):
    """flips vector2 on x axis"""
    return vec * Vector2(-1, 1)


def draw_torso():
    """base torso"""
    center, radius = constants["center"], constants["radius"]
    torso = constants["torso"]
    shadow = torso["shadow"]
    no_shadow = (180 - shadow) / 2

    # red circle
    peon.color(0.8, 0, 0)
    peon.tp(center + Vector2(radius, 0), 90)
    peon.pd()

    peon.begin_fill()
    peon.circle(radius)
    peon.end_fill()

    peon.pu()
    peon.circle(radius, no_shadow)
    peon.fillcolor("red")
    peon.pd()

    # circle highlight
    peon.begin_fill()
    peon.circle(radius, shadow)
    peon.follow_path(
        Bezier(peon.pos(), center + torso["shadow_dip"], mirror(peon.pos())).map_eq(20)
    )
    peon.end_fill()

    # pants
    peon.tp(center - Vector2(radius, 0), 270)
    peon.color("black")

    peon.begin_fill()
    peon.circle(radius, no_shadow)
    peon.pencolor(0.5, 0.5, 0.5)
    peon.circle(radius, shadow)
    peon.pencolor(0, 0, 0)
    peon.circle(radius, no_shadow)
    # fmt: off
    peon.follow_path(
        Bezier(peon.pos(), center + torso["stomach_arch"], mirror(peon.pos())).map_eq(20)
    )
    # fmt: on
    peon.end_fill()


def draw_legs():
    """left and right leg"""
    radius = constants["radius"]
    legs = constants["legs"]

    # I got really lazy here sorry
    # leftmost
    peon.seth(270)
    peon.pencolor(0.5, 0.5, 0.5)
    peon.pu()
    peon.circle(radius, legs["principal"])
    peon.rt(90)
    peon.pd()

    peon.forward(50)
    peon.lt(20)
    peon.forward(30)
    peon.rt(60)
    peon.forward(60)
    peon.seth(0)
    peon.forward(120)
    peon.lt(110)
    peon.forward(30)
    peon.pu()

    # rightmost
    peon.tp(constants["center"] + Vector2(radius, 0), 90)
    peon.circle(radius, -legs["principal"])
    peon.rt(90)
    peon.pd()

    peon.forward(50)
    peon.rt(20)
    peon.forward(30)
    peon.lt(60)
    peon.forward(60)
    peon.seth(180)
    peon.forward(120)
    peon.rt(110)
    peon.forward(30)
    peon.pu()


def draw_details():
    """draws random details"""
    center = constants["center"]
    radius = constants["radius"]
    details = constants["details"]
    peon.color(0.8, 0.8, 0.8)

    # buttons
    for button in details["buttons"]:
        peon.tp(center + button)
        peon.dot(30)

    # yellow thingies
    peon.tp(center + Vector2(radius, 0), 90)
    peon.color(1, 0.8, 0)
    peon.circle(radius, 60)

    peon.begin_fill()
    peon.pd()
    peon.circle(radius, 60)

    def trace_nacho(tip_coord, destination):
        """makes yellow thing"""
        # fmt: off
        peon.follow_path(
            Bezier(peon.pos(), (push := tip_coord + Vector2(0, 20)), tip_coord).map_eq(10)
        )
        # fmt: on
        peon.follow_path(Bezier(peon.pos(), push, destination).map_eq(10))

    fin = mirror(peon.pos())
    trace_nacho(
        center + details["yellow_thingies"][0],
        center + Vector2(0, radius - constants["face"]["radius"]),
    )
    trace_nacho(center + details["yellow_thingies"][1], fin)

    peon.end_fill()


def draw_face():
    """draws that beautiful face"""
    center, radius = constants["center"], constants["radius"]
    face = constants["face"]

    face_pos = center + Vector2(0, radius)
    peon.pencolor(0.8, 0.4, 0.4)
    peon.fillcolor("pink")

    # face
    peon.tp(face_pos + Vector2(face["radius"], 0), 90)
    peon.begin_fill()
    peon.circle(face["radius"])
    peon.end_fill()

    # smile
    peon.color(1, 1, 1)
    smile_radius = face["radius"] - face["smile_inset"]
    start = face_pos - Vector2(smile_radius)
    peon.tp(start, 270)
    peon.begin_fill()
    peon.circle(smile_radius, 180)
    peon.end_fill()

    peon.seth(180)
    end = peon.pos()
    peon.pencolor("black")

    for step in range(1, face["teeth"]):
        coord = lerp(start, end, step / face["teeth"])
        peon.tp(coord, 270)
        peon.forward(math.sqrt(smile_radius ** 2 - abs(coord.x - face_pos.x) ** 2))

    # glasses
    peon.color(0, 0, 0.4)
    peon.tp(face_pos + face["glasses"][0])
    peon.dot(25)
    peon.tp(face_pos + face["glasses"][1])
    peon.dot(25)
    peon.goto(face_pos + face["glasses"][0])

    # got lazy again
    peon.color("brown")
    peon.tp(face_pos)
    peon.begin_fill()
    for _ in range(2):
        peon.lt(10)
        peon.forward(face["moustache_length"])
        peon.rt(100)
        peon.forward(face["moustache_length"] * math.sin(math.radians(10)) * 2)
        peon.goto(*face_pos)
        peon.seth(180)
    peon.end_fill()

    # nose
    peon.color(1, 0.4, 0.4)
    peon.dot(15)

def main():
    """drawing"""
    peon.canvas.bgcolor(0, 0, 0)
    draw_torso()
    draw_legs()
    draw_details()
    draw_face()
    animation_loop()


main()

turtle.done()
