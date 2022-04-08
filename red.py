import random
from constants import *

def move(turt, world):
    if turt.index == 0:
        # BASIC OFFENSE CODE
        x = world.flag_dist(turt, RED, X)
        y = world.flag_dist(turt, RED, Y)
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
        ## BASIC DEFENSE CODE
        x = world.flag_dist(turt, BLUE, X)
        y = world.flag_dist(turt, BLUE, Y)

        if y < 1:
            turt.register_move(SOUTH)
            return
        elif y > 1 :
            turt.register_move(NORTH)
            return
        if x > 0:
            turt.register_move(EAST)
            return
        elif x < 0:
            turt.register_move(WEST)
            return
