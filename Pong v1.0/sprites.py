
import turtle

class Sprite(turtle.Turtle):
    def __init__(self, x, y, shape = 'square', color = 'white'):
        turtle.Turtle.__init__(self)
        self.shape(shape)
        self.color(color)
        self.penup()
        self.goto(x, y)

class Paddle(Sprite):
    def __init__(self, x, y, shape = 'square', color = 'white'):
        Sprite.__init__(self, x, y, shape, color)
        self.setheading(90)
        self.length = 10
        # stretch: 1.0 = 20px (caly wymiar figury), 1.0 = 10px (liczac od srodka figury)
        self.shapesize(stretch_wid = 1.0, stretch_len = self.length, outline = None)
        self.dir = 0
        self.step = 10
        self.boundary = 'none'

    def move(self):
        self.fd(self.dir * self.step)
        # wykrywanie granic
        if self.ycor() + 10 * self.length >= 300:
            self.dir = 0
            self.boundary = 'upper'
        if self.ycor() - 10 * self.length <= -300:
            self.dir = 0
            self.boundary = 'bottom'

    def up(self):
        # zmiana kierunku na bezruch lub w gore
        if self.boundary == 'none' and self.dir < 1:
            self.dir += 1
        # odklejenie od dolu
        if self.boundary == 'bottom':
            self.boundary = 'none'
            self.dir = 1

    def down(self):
       # zmiana kierunku na bezruch lub w dol
       if self.boundary == 'none' and self.dir > -1:
            self.dir -= 1
       # odklejenie od gory
       if self.boundary == 'upper':
           self.boundary = 'none'
           self.dir = -1

class Player(Paddle):
    def __init__(self, x, y, shape = 'square', color = 'white'):
        Paddle.__init__(self, x, y, shape, color)
        self.type = 'player'

class Opponent(Paddle):
    def __init__(self, x, y, shape = 'square', color = 'white'):
        Paddle.__init__(self, x, y, shape, color)
        self.type = 'opponent'
        self.dir = 1
        self.step = 12

class Ball(Sprite):
    def __init__(self, x, y, shape = 'circle', color = 'white'):
        Sprite.__init__(self, x, y, shape, color)
        self.radius = 1.0
        # stretch: 1.0 = 20px (caly wymiar figury), 1.0 = 10px (liczac od srodka figury)
        self.shapesize(stretch_wid = self.radius, stretch_len = self.radius, outline = None)
        self.setheading(0)
        self.speed = 10 # multiplikator wektora ruchu
        # skladowe wektora ruchu
        self.dx = -1.0
        self.dy = -0.2

    def move(self):
        self.goto(self.xcor() + self.speed * self.dx, self.ycor() + self.speed * self.dy)

    def isCollision(self, paddle):
        # kolizja z paletka gracza
        if paddle.type == 'player':
            player = paddle
            if self.xcor() - 10 * self.radius <= player.xcor() + 10 and \
            player.ycor() - 10 * player.length <= self.ycor() and \
            player.ycor() + 10 * player.length >= self.ycor():
                return True
            else:
                return False
        # kolizja z paletka przeciwnika
        if paddle.type == 'opponent':
            opponent = paddle
            if self.xcor() + 10 * self.radius >= opponent.xcor() - 10 and \
            opponent.ycor() - 10 * opponent.length <= self.ycor() and \
            opponent.ycor() + 10 * opponent.length >= self.ycor():
                return True
            else:
                return False

    # odbicie pilki paletka
    def bounceBack(self, paddle):
        if paddle.dir == 1:
            if self.dy < 0:
                self.dy = -1 * self.dy
                self.dx = -1 * self.dx
            elif self.dy > 0:
                self.dy = 1.2 * self.dy
                self.dx = - self.dx
            else:
                self.dy = 0.3
                self.dx = - self.dx

        elif paddle.dir == -1:
            if self.dy > 0:
                self.dy = -1 * self.dy
                self.dx = -1 * self.dx
            elif self.dy < 0:
                self.dy = 1.2 * self.dy
                self.dx = - self.dx
            else:
                self.dy = -0.3
                self.dx = - self.dx

        else:
            self.dx = - self.dx
