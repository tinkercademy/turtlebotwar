import turtle
import random
import math
from constants import *
import time
import blue
import red

#ws = turtle.Screen()
#ws.screensize(WIDTH, HEIGHT)

NO_BOTS = 2
blue_bots = []
red_bots = []
ball = None
world = None

class TurtleBot:
    def __init__(self, color, index, world):
        t = turtle.Turtle()
        t.color(color)
        t.shape("turtle")
        t.pu()
        self.t = t
        self.color = color
        self.index = index
        self.registered_move = -1
        self.world = world
        self.teleport_random()
        self.draw()

    def x(self):
        return self.pos['x']

    def y(self):
        return self.pos['y']

    def in_home_territory(self):
        return (self.color == RED and self.pos['y'] >= BOARD_HEIGHT/2) or (self.color == BLUE and self.pos['y'] < BOARD_HEIGHT/2)

    def teleport_random(self):
        if self.color == RED:
            while True:
                self.pos = { 'x': random.randint(0, BOARD_WIDTH-1) , 'y': random.randint(BOARD_HEIGHT/2, BOARD_HEIGHT-1) }
                # We can't teleport onto the opponent flag
                if not (world.blue_flag_pos[0] == self.pos['x'] and world.blue_flag_pos[1] == self.pos['y']):
                    break

        elif self.color == BLUE:
            while True:
                self.pos = { 'x': random.randint(0, BOARD_WIDTH-1) , 'y': random.randint(0, BOARD_HEIGHT/2 - 1) }
                # We can't teleport onto the opponent flag
                if not (world.red_flag_pos[0] == self.pos['x'] and world.red_flag_pos[1] == self.pos['y']):
                    break

    def set_program(self, func):
        self.func = func

    def is_valid_move(self, move):
        in_bounds = (move == EAST and self.pos['x'] < BOARD_WIDTH-1) or \
                    (move == NORTH and self.pos['y'] < BOARD_HEIGHT-1) or \
                    (move == WEST and self.pos['x'] > 0) or \
                    (move == SOUTH and self.pos['y'] > 0)

        # Make a local move to check if we are going to move onto the flag
        local_x, local_y = self.pos['x'], self.pos['y']
        if move == EAST:
            local_x += 1
        elif move == NORTH:
            local_y += 1
        elif move == WEST:
            local_x -= 1
        elif move == SOUTH:
            local_y -= 1
        fx, fy = -1, -1

        if self.color == RED:
            fx, fy = self.world.blue_flag_pos
        elif self.color == BLUE:
            fx, fy = self.world.red_flag_pos
        # If we are touching our opponent's flag, the move is disallowed
        flag_touch = fx == local_x and fy == local_y

        return in_bounds and not flag_touch

    def capture_flag(self):
        # Check if we captured a flag
        fx, fy = -1, -1
        if self.color == BLUE:
            fx, fy = self.world.blue_flag_pos
        elif self.color == RED:
            fx, fy = self.world.red_flag_pos

        if self.pos['x'] == fx and self.pos['y'] == fy:
            # we reached our flag!
            if self.color == BLUE:
                world.blue_score += 10
            elif self.color == RED:
                world.red_score += 10
            self.teleport_random()
            world.reset_flag(self.color)


    def register_move(self, move):
        self.registered_move = move if self.is_valid_move(move) else -1
        if self.registered_move == EAST:
            self.t.setheading(0)
        elif self.registered_move == NORTH:
            self.t.setheading(90)
        elif self.registered_move == WEST:
            self.t.setheading(180)
        elif self.registered_move == SOUTH:
            self.t.setheading(270)


    def move(self):
        if self.registered_move == EAST:
            self.pos['x'] += 1
        elif self.registered_move == NORTH:
            self.pos['y'] += 1
        elif self.registered_move == WEST:
            self.pos['x'] -= 1
        elif self.registered_move == SOUTH:
            self.pos['y'] -= 1

        self.registered_move = -1

    def draw(self):
        x = self.pos['x'] * WIDTH/BOARD_WIDTH - WIDTH / 2 + WIDTH/20 - 5
        y = self.pos['y'] * HEIGHT/BOARD_HEIGHT - HEIGHT/ 2 + HEIGHT/20
        self.t.goto(x,y)

class TurtleWorld:
    def __init__(self, size):
        self.size = size
        self.t = turtle.Turtle()
        self.t.ht()
        self.score_t = turtle.Turtle()
        self.score_t.pu()
        self.score_t.ht()

        self.blue_flag = turtle.Turtle()
        self.blue_flag.shape("arrow")
        self.blue_flag.color(BLUE)
        self.blue_flag.pensize(5)

        self.red_flag = turtle.Turtle()
        self.red_flag.shape("arrow")
        self.red_flag.color(RED)
        self.red_flag.pensize(5)

        self.reset_flag(BLUE)
        self.reset_flag(RED)
        self.blue_score = 0
        self.red_score = 0

    def flag_dist(self, bot, color, axis):
        fx, fy = -1, -1
        if color == RED:
            fx, fy = self.red_flag_pos
        elif color == BLUE:
            fx, fy = self.blue_flag_pos
        if fx == -1:
            return -999

        distance = 0
        if axis == X:
            distance = fx - bot.pos['x']
        elif axis == Y:
            distance = fy - bot.pos['y']

        return distance

    def ball_dist(self, bot, axis):
        bx, by = ball.pos['x'], ball.pos['y']

        distance = 0
        if axis == X:
            distance = bx - bot.pos['x']
        elif axis == Y:
            distance = by - bot.pos['y']

        return distance

    def turtle_dist(self, bot, color, index, axis):
        ox, oy = -1, -1
        other_bot = None
        if color == BLUE:
            for b in blue_bots:
                if b.index == index:
                    other_bot = b
                    break
        elif color == RED:
            for b in red_bots:
                if b.index == index:
                    other_bot = b
                    break
        if other_bot is None:
            return -999

        distance = 0
        if axis == X:
            distance = other_bot.pos['x'] - bot.pos['x']
        elif axis == Y:
            distance = other_bot.pos['y'] - bot.pos['y']

        return distance


    def reset_flag(self, color):
        if color == BLUE:
            # Blue Flag reset
            # generated in red territory
            while True:
                x = random.randint(0, BOARD_WIDTH-1)
                y = random.randint(math.floor(3 * BOARD_HEIGHT / 4 ), BOARD_HEIGHT-1)
                # We can't teleport onto a red turtle
                conflict = False 
                for bot in red_bots:
                    if bot.pos['x'] == x and bot.pos['y'] == y:
                        conflict = True
                if not conflict:
                    break
            self.blue_flag_pos = (x,y)
            x = x * WIDTH/BOARD_WIDTH - WIDTH / 2 + WIDTH/40
            y = y *  HEIGHT/BOARD_HEIGHT - HEIGHT/ 2 + 5
            self.blue_flag.goto(x,y)
            self.blue_flag.clear()
            self.blue_flag.goto(x,y+20)

        if color == RED:
            # Red Flag reset
            # generated in blueterritory

            while True:
                x = random.randint(0, BOARD_WIDTH-1)
                y = random.randint(0, math.floor(BOARD_HEIGHT / 4 ))
                # We can't teleport onto a blue turtle
                conflict = False 
                for bot in blue_bots:
                    if bot.pos['x'] == x and bot.pos['y'] == y:
                        conflict = True
                if not conflict:
                    break
            self.red_flag_pos = (x,y)
            x = x * WIDTH/BOARD_WIDTH - WIDTH / 2 + WIDTH/40
            y = y *  HEIGHT/BOARD_HEIGHT - HEIGHT/ 2  + 5
            self.red_flag.goto(x,y)
            self.red_flag.clear()
            self.red_flag.goto(x,y+20)

    def get_flag_pos(self, colour):
        if colour == BLUE:
            return self.blue_flag_pos
        elif colour == RED:
            return self.red_flag_pos

        return (-1, -1)

    def get_size(self):
        return self.size

    def draw_score(self):
        self.score_t.clear()
        self.score_t.color(BLUE)
        self.score_t.goto(10, -HEIGHT/BOARD_HEIGHT)
        self.score_t.write("BLUE: " + str(world.blue_score), move=False, align="left", font=("Arial", 16, "normal"))
        self.score_t.goto(10, 0)
        self.score_t.color(RED)
        self.score_t.write("RED: " + str(world.red_score), move=False, align="left", font=("Arial", 16, "normal"))

        self.score_t.goto(-5 * WIDTH/BOARD_WIDTH, 0)
        self.score_t.color("black")
        self.score_t.write("Turn: " + str(turn), move=False, align="left", font=("Arial", 16, "normal"))


    def draw_grid(self):
        # draw row lines
        for y in range(int(-HEIGHT/2), int(HEIGHT/2) + 1, int(HEIGHT/self.size)):
            self.t.pu()
            self.t.goto(-WIDTH/2, y)
            self.t.pd()
            if y < BOARD_HEIGHT/2:
                self.t.color('blue')
            else:
                self.t.color('red')

            self.t.goto(WIDTH/2, y)
        # draw column lines
        for x in range(int(-WIDTH/2), int(WIDTH/2) + 1, int(WIDTH/self.size)):
            self.t.pu()
            self.t.goto(x, -HEIGHT/2)
            self.t.pd()
            self.t.color('blue')
            self.t.goto(x, 0)
            self.t.color('red')
            self.t.goto(x, HEIGHT/2)


class Ball():
    def __init__(self):
        self.t= turtle.Turtle()
        self.t.shape('circle')
        self.t.pu()
        self.teleport_random()

    def _conflict(self, bot):
        return self.pos['x'] == bot.x() and self.pos['y'] == bot.y()

    def teleport_random(self):
        while True:
            conflict = False
            self.pos = { 'x': random.randint(0, BOARD_WIDTH-1) , 'y': random.randint(0, BOARD_HEIGHT-1) }

            for bot in blue_bots + red_bots:
                if self._conflict(bot):
                    conflict = True

            if self.pos['x'] == world.blue_flag_pos[0] and self.pos['y'] == world.blue_flag_pos[1]:
                conflict = True

            if self.pos['x'] == world.red_flag_pos[0] and self.pos['y'] == world.red_flag_pos[1]:
                conflict = True

            if not conflict:
                break


    def move(self, ratio=0.05):
        # in the move function, we just check if a bot is on top of us
        # if there is, we increase the score and teleport ourselves away
        for bot in blue_bots + red_bots:
            if self.pos['x'] == bot.x() and self.pos['y'] == bot.y():
                self.teleport_random()
                if bot.color == BLUE:
                    world.blue_score += 1
                elif bot.color == RED:
                    world.red_score += 1

        if random.random() < ratio:
            self.teleport_random()


    def draw(self):
        x = self.pos['x'] * WIDTH/BOARD_WIDTH - WIDTH / 2 + WIDTH/20
        y = self.pos['y'] * HEIGHT/BOARD_HEIGHT - HEIGHT/ 2 + HEIGHT/20
        self.t.goto(x,y)


# Initialization Code
turtle.tracer(0)
world = TurtleWorld(BOARD_WIDTH)
for i in range(NO_BOTS):
    blue_t = TurtleBot(BLUE, i, world)
    blue_bots.append(blue_t)
    red_t = TurtleBot(RED, i, world)
    red_bots.append(red_t)
ball = Ball()

def calc_distance(bot1, bot2):
    return abs(bot1.pos['x'] - bot2.pos['x']) + abs(bot1.pos['y'] - bot2.pos['y'])

def resolve_move_conflicts():
    # Resolve move conflicts
    for bot in blue_bots + red_bots:
        for other_bot in blue_bots + red_bots:
            if bot != other_bot: # there is no move conflict for the bot with itself
                distance = calc_distance(bot, other_bot)
                if distance == 0:
                    # transport both bots home
                    bot.teleport_random()
                    other_bot.teleport_random()

                elif distance == 1:
                    # todo - we check if they crossed each other
                    if ((bot.pos['x'] > other_bot.pos['x'] \
                        and bot.registered_move == EAST and other_bot.registered_move == WEST) or \
                        (bot.pos['x'] < other_bot.pos['x'] \
                         and bot.registered_move == WEST and other_bot.registered_move == EAST) or \
                        (bot.pos['y'] > other_bot.pos['y'] \
                         and bot.registered_move == NORTH and other_bot.registered_move == SOUTH) or \
                        (bot.pos['y'] < other_bot.pos['y'] \
                         and bot.registered_move == SOUTH and other_bot.registered_move == NORTH)):
                        other_bot.teleport_random()
                        bot.teleport_random()

def run_step():
    for bot in blue_bots:
        blue.move(bot, world)
        bot.move()

    for bot in red_bots:
        red.move(bot, world)
        bot.move()

    resolve_move_conflicts()

    ball.move()
    
    for bot in blue_bots + red_bots:
        bot.draw()

    ball.draw()

    world.draw_score()
    turtle.update()


world.draw_grid()
turn = TURNS
while True:
    run_step()
    time.sleep(0.2)
    turn += -1

    if turn < 0:
        break

#ws.exitonclick()
