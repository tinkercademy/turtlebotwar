import random
from constants import *

##### RED-BLUE AREA ########

#############################
# RED AREA            (9,9)
#
#
#
# (0, 5)
#############################
# BLUE AREA
#
#
#
# (0, 0)
#############################

# API
#
# world.flag_dist(turtle, colour, axis)
# e.g. world.flag_dist(turtle, BLUE, X)
# returns distance to flag in that axis
#
# world.turtle_dist(turtle, colour, index, axis)
# e.g. world.turtle_dist(turtle, RED, 0, Y)
# returns distance to turtle in that axis
#
# turtle.register_move(direction)
# e.g. turt.register_move(EAST)
#
# turtle.capture_flag()
# if you're the flag, you can capture the flag


def move(turt, world):
    if turt.index == 0:
        x = world.flag_dist(turt, BLUE, X)
        y = world.flag_dist(turt, BLUE, Y)
        if x > 0:
            turt.register_move(EAST)
            return
        elif x < 0:
            turt.register_move(WEST)
            return

        if y > 0:
            turt.register_move(NORTH)
            return
        elif y < 0:
            turt.register_move(SOUTH)
            return

        if x == 0 and y == 0:
            turt.capture_flag()

    elif turt.index == 1:
        turt.register_move(random.randint(0,3))
