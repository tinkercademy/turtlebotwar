import random
from constants import *

##### RED-BLUE AREA ########

#############################
# RED AREA            (19,19)
#
#
#
# (0, 10)
#############################
# BLUE AREA
#
#
#
# (0, 0)
#############################

# API
#
# World Coordinates
# world.flag_dist(turtle, colour, axis)
# e.g. world.flag_dist(turtle, "blue", X)
# returns distance to flag in that axis
#
# world.turtle_dist(turtle, colour, index, axis)
# e.g. world.turtle_dist(turtle, "red", 0, Y)
# returns distance to turtle in that axis

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
