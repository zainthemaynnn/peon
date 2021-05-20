"""
this is where the drawing takes place
compared to the rest, this is pretty rushed and therefore long
just because of the sheer tediousness of mapping everything properly
have fun in this rat's nest...
"""

import turtle
import math
from asyncio import sleep, run
from peon import Peon
from geometry.coordinate import Vector2, lerp
from geometry.bezier import Bezier

constants = {
    "center": Vector2(0, -100),
    "radius": 150,
    "torso": {
        "stomach_arch": Vector2(0, 20),
        "shadow": 140,
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
    "arms": {"principal": 20, "arm_len": 50, "fore_len": 50, "hand_radius": 40},
    "toss": {
        "height": Vector2(0, 500),
        "points": 20,
        "threshold": 3,
        "fps": 24,
        "break": 0,
    },
}

peon = Peon()


def mirror(vec):
    """flips vector2 over x axis of center"""
    return vec * Vector2(-1, 1) + Vector2(constants["center"].x, 0)


def mirror_path(coords):
    """mirrors all coordinates in a path"""
    return [mirror(coord) for coord in coords]


def draw_torso():
    """base torso"""
    center, radius = constants["center"], constants["radius"]
    torso = constants["torso"]
    shadow = torso["shadow"]
    no_shadow = (180 - shadow) / 2

    # red circle
    peon.color("firebrick")
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
    peon.pencolor("dark gray")
    peon.circle(radius, shadow)
    peon.pencolor("black")
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
    peon.pencolor("dark gray")
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
    peon.forward(20)
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
    peon.forward(20)
    peon.pu()


def draw_details():
    """draws random details"""
    center = constants["center"]
    radius = constants["radius"]
    details = constants["details"]
    peon.color("silver")

    # buttons
    for button in details["buttons"]:
        peon.tp(center + button)
        peon.dot(30)

    # yellow thingies
    peon.tp(center + Vector2(radius, 0), 90)
    peon.color("gold")
    peon.circle(radius, 60)

    peon.begin_fill()
    peon.pd()
    peon.circle(radius, 60)

    # fmt: off
    def trace_nacho(tip_coord, destination):
        """makes yellow thing, small offset with a bezier to make it curved"""
        peon.follow_path(
            Bezier(peon.pos(), (push := tip_coord + Vector2(0, 20)), tip_coord).map_eq(10)
        )
        peon.follow_path(Bezier(peon.pos(), push, destination).map_eq(10))
    # fmt: on

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
    peon.pencolor("light coral")
    peon.fillcolor("pink")

    # face
    peon.tp(face_pos + Vector2(face["radius"], 0), 90)
    peon.begin_fill()
    peon.circle(face["radius"])
    peon.end_fill()

    # smile
    peon.color("white")
    smile_radius = face["radius"] - face["smile_inset"]
    start = face_pos - Vector2(smile_radius)
    peon.tp(start, 270)
    peon.begin_fill()
    peon.circle(smile_radius, 180)
    peon.end_fill()

    end = peon.pos()
    peon.color("black")

    for step in range(1, face["teeth"]):
        coord = lerp(start, end, step / face["teeth"])
        peon.tp(coord, 270)
        peon.forward(math.sqrt(smile_radius ** 2 - (coord.x - face_pos.x) ** 2))

    # glasses
    peon.color("midnight blue")
    peon.tp(face_pos + face["glasses"][0])
    peon.dot(25)
    peon.goto(face_pos + face["glasses"][1])
    peon.dot(25)

    peon.color("brown")
    peon.tp(face_pos)
    peon.begin_fill()

    # moustache (got lazy again)
    dist = face["moustache_length"] * math.sin(math.radians(10)) * 2
    registered = [peon.pos()]

    def trace(turn, n_deg, distance):
        """basically helps copy the other side of the moustache"""
        turn(n_deg)
        peon.forward(distance)
        registered.append(mirror(peon.pos()))

    trace(peon.lt, 10, face["moustache_length"])
    trace(peon.lt, 20, dist)
    trace(peon.rt, 120, dist / 2)
    trace(peon.lt, 60, dist)
    peon.pencolor("maroon")
    trace(peon.rt, 120, dist)
    trace(peon.lt, 60, dist / 2)
    trace(peon.rt, 120, dist)
    trace(peon.lt, 20, face["moustache_length"])
    peon.end_fill()

    peon.pencolor("brown")
    peon.begin_fill()
    peon.follow_path(registered[:5])
    peon.pencolor("maroon")
    peon.follow_path(registered[4:])
    peon.end_fill()

    # nose
    peon.color("light coral")
    peon.dot(15)


# from here on out I got really tired :(
# I apologize in advance for the atrocities comitted below
# you know, worse than the ones displayed above
def draw_arms():
    """draws arms"""
    radius = constants["radius"]
    arms = constants["arms"]

    peon.tp(constants["center"] + Vector2(radius, 0), 90)
    peon.pu()
    peon.circle(radius, arms["principal"])
    peon.pd()

    peon.pencolor("firebrick")
    peon.fillcolor("red")
    peon.begin_fill()
    peon.begin_poly()

    final = peon.pos()
    peon.circle(radius, 20)

    curve_0 = Bezier(
        peon.pos(),
        mid := peon.pos() + Vector2(1, 0) * arms["arm_len"],
        mid + Vector2(1 / math.sqrt(2), 1 / math.sqrt(2)) * arms["fore_len"],
    ).map_eq(5)
    peon.follow_path(curve_0)

    peon.rt(70)
    peon.forward(20)
    hand_pos, hand_dir = peon.pos(), peon.heading()
    peon.forward(20)

    # didn't feel like calculating it for real
    # an irregular arm shape is nicer anyways
    mid_approx = mid + Vector2(25, -25)
    curve_1 = Bezier(peon.pos(), mid_approx, final).map_eq(5)
    peon.follow_path(curve_1)

    peon.end_fill()
    peon.end_poly()
    arm = mirror_path(peon.get_poly())

    peon.pencolor("light gray")
    peon.fillcolor("white")
    peon.tp(hand_pos, hand_dir)

    peon.begin_fill()
    peon.begin_poly()
    peon.circle(arms["hand_radius"])
    peon.end_fill()
    peon.end_poly()

    hand = mirror_path(peon.get_poly())

    peon.pu()
    peon.lt(90)
    peon.forward(arms["hand_radius"])
    hand_center_0, hand_center_1 = peon.pos(), mirror(peon.pos())
    peon.pd()

    peon.pencolor("firebrick")
    peon.fillcolor("red")
    peon.follow_path(arm)
    peon.end_fill()

    peon.pencolor("light gray")
    peon.fillcolor("white")
    peon.follow_path(hand)
    peon.end_fill()

    return hand_center_0, hand_center_1


async def animation_loop(hand0, hand1):
    """this is freakin janky"""

    c_toss = constants["toss"]

    emeralds = []
    # create backwards so blue stays on top like the original
    for i in range(6, 0, -1):
        emerald = Peon()
        emerald.ht()
        emerald.goto(hand0)
        emerald.screen.register_shape(f"resources/emeralds/{i}.gif")
        emerald.shape(f"resources/emeralds/{i}.gif")
        emerald.speed(0)
        emeralds.append(emerald)

    emeralds = emeralds[::-1]

    async def toss(path):
        frames = 0
        e_count = iter(emeralds)
        active = []
        paths = []
        running = True

        while running:
            if frames == 0:
                frames = c_toss["threshold"]
                try:
                    emerald = next(e_count)
                    emerald.st()
                    active.append(emerald)
                    paths.append(iter(path))
                except StopIteration:
                    # ez
                    frames = -1

            for emerald, local_path in zip(active, paths):
                try:
                    emerald.goto(next(local_path))
                except StopIteration:
                    if emerald == emeralds[-1]:
                        running = False
                        break

                    active.pop(0)
                    paths.pop(0)

            frames -= 1
            await sleep(1 / c_toss["fps"])

    path0 = Bezier(hand0, constants["center"] + c_toss["height"], hand1).map_eq(
        c_toss["points"]
    )
    path1 = path0[::-1]

    while True:
        await toss(path0)
        await sleep(c_toss["break"])
        await toss(path1)
        await sleep(c_toss["break"])


async def main():
    """drawing"""
    peon.canvas.bgcolor("black")
    draw_torso()
    draw_legs()
    draw_details()
    draw_face()
    hand0, hand1 = draw_arms()
    peon.ht()
    await animation_loop(hand0, hand1)


run(main())

turtle.done()
