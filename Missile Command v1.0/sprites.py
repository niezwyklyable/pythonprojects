
import turtle
import math

class Sprite(turtle.Turtle):
    def __init__(self, x, y, color, shape):
        turtle.Turtle.__init__(self)
        self.color(color)
        self.shape(shape)
        self.penup()
        self.goto(x, y)

    def isCollision(self, other):
        if abs(self.xcor() - other.xcor()) < 5 and \
            abs(self.ycor() - other.ycor()) < 5:
            return True
        else:
            return False

class City(Sprite):
    def __init__(self, x, y, color, shape):
        Sprite.__init__(self, x, y, color, shape)

class Silo(Sprite):
    def __init__(self, x, y, color, shape):
        Sprite.__init__(self, x, y, color, shape)

class Center(Sprite):
    def __init__(self, x, y, color, shape):
        Sprite.__init__(self, x, y, color, shape)
        self.radius = 0.2
        self.shapesize(stretch_wid = self.radius, stretch_len = self.radius, outline = None)

class PlayerMissile(Center):
    def __init__(self, x, y, color, shape, targetX, targetY):
        Center.__init__(self, x, y, color, shape)
        self.targetX = targetX
        self.targetY = targetY
        self.step = 4
        self.status = 'normal'
        if targetX > x:
            self.setheading(math.degrees(math.atan(abs(targetY - y) / abs(targetX - x))))
        elif targetX < x:
            self.setheading(180 - math.degrees(math.atan(abs(targetY - y) / abs(targetX - x))))
        else:
            self.setheading(90)
        self.pendown()
        if x == -350:
            self.pos = 'left'
        elif x == 350:
            self.pos = 'right'
        else:
            self.pos = 'middle'

    def move(self):
        # sprawdza czy pocisk dotarl do celu + zabezpieczenie jesli nie dotarl
        if abs(self.xcor() - self.targetX) < 5 and abs(self.ycor() - self.targetY) < 5 or \
            self.pos == 'left' and (self.xcor() <= -400 or self.xcor() >= -175) or \
            self.pos == 'middle' and (self.xcor() <= -175 or self.xcor() >= 175) or \
            self.pos == 'right' and (self.xcor() <= 175 or self.xcor() >= 400):
            self.status = 'explode'
        else:
            self.fd(self.step)

    def explosion(self):
        if self.status == 'explode':
            self.radius += 0.05
        if self.status == 'fadeOut':
            self.radius -= 0.05
        if self.status == 'explode' and self.radius >= 3.0:
            self.status = 'fadeOut'
        if self.status == 'fadeOut' and self.radius <= 0.2:
            self.status = 'end'
        self.shapesize(stretch_wid = self.radius, stretch_len = self.radius, outline = None)
        
    def isCollision(self, other):
        if abs(self.xcor() - other.xcor()) < 10 * self.radius and \
            abs(self.ycor() - other.ycor()) < 10 * self.radius:
            return True
        else:
            return False

class EnemyMissile(Center):
    def __init__(self, x, y, color, shape, targetX, targetY):
        Center.__init__(self, x, y, color, shape)
        self.step = 2
        self.status = 'normal'
        if targetX > x:
            self.setheading(- math.degrees(math.atan(abs(targetY - y) / abs(targetX - x))))
        elif targetX < x:
            self.setheading(180 + math.degrees(math.atan(abs(targetY - y) / abs(targetX - x))))
        else:
            self.setheading(-90)
        self.pendown()

    def move(self):
        self.fd(self.step)

    def explosion(self):
        if self.status == 'explode':
            self.radius += 0.05
        if self.status == 'fadeOut':
            self.radius -= 0.05
        if self.status == 'explode' and self.radius >= 3.0:
            self.status = 'fadeOut'
        if self.status == 'fadeOut' and self.radius <= 0.2:
            self.status = 'end'
        self.shapesize(stretch_wid = self.radius, stretch_len = self.radius, outline = None)
