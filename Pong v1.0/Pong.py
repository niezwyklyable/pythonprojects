
# inkludowanie modulow
import turtle
import time
import winsound
import random

# inkludowanie klas
from game import Game
from sprites import Player
from sprites import Opponent
from sprites import Ball

# ustawienia globalne
turtle.bgcolor('black')
turtle.ht()
turtle.setup(900, 700) # wymiary okna gry
turtle.title('Pong by AW v1.0')
turtle.tracer(0)

# stworzenie obiektow
game = Game(11) # (goalScore)
player = Player(-380, 0) # (x, y)
opponent = Opponent(380, 0) # (x, y)
ball = Ball(0, 0) # (x, y)

# ustawienia nasluchow (sterowanie)
turtle.listen()
turtle.onkey(player.up,'Up')
turtle.onkey(player.down,'Down')

def restart():
    ans = input('Play again? (input \'y\' if yes): ')
    if ans == 'y':
        game.restart()
        player.length = 10
        player.shapesize(stretch_wid = 1.0, stretch_len = player.length, outline = None)
        player.sety(0)
        player.dir = 0
        player.boundary = 'none'
        opponent.step = 12
        opponent.sety(0)
        opponent.dir = 1
        opponent.boundary = 'none'
        ball.goto(0, 0)
        ball.speed = 10
        ball.dx = -1.0
        ball.dy = -0.2
        turtle.update()
        time.sleep(2)
    else:
        return False

while True:
    turtle.update() # odmalowanie klatki
    time.sleep(0.04) # opoznienie [s]

    player.move()
    opponent.move()
    ball.move()
    game.counter += 1
    
    # kolizja z paletka gracza
    if ball.isCollision(player):
        winsound.PlaySound('bounce.wav', winsound.SND_ASYNC)
        ball.setx(player.xcor() + 10 + 10 * ball.radius) # wyrownanie krawedzi obiektow
        ball.bounceBack(player) # zmiana kierunku

    # kolizja z paletka przeciwnika
    if ball.isCollision(opponent):
        winsound.PlaySound('bounce.wav', winsound.SND_ASYNC)
        ball.setx(opponent.xcor() - 10 - 10 * ball.radius) # wyrownanie krawedzi obiektow
        ball.bounceBack(opponent) # zmiana kierunku
    
    # kolizja z gornym borderem
    if ball.ycor() + 10 * ball.radius >= 300:
        winsound.PlaySound('bounce.wav', winsound.SND_ASYNC)
        ball.sety(300 - 10 * ball.radius)
        ball.dy = - ball.dy

    # kolizja z dolnym borderem
    if ball.ycor() - 10 * ball.radius <= -300:
        winsound.PlaySound('bounce.wav', winsound.SND_ASYNC)
        ball.sety(-300 + 10 * ball.radius)
        ball.dy = - ball.dy

    # kolizja z prawym borderem
    if ball.xcor() >= 400:
        ball.goto(opponent.xcor() - 10 - 10 * ball.radius, opponent.ycor())
        ball.dx = - 1.0
        if random.randint(1, 2) == 1:
            ball.dy = float(random.randint(1, 5)) / 10.0
        else:
            ball.dy = - float(random.randint(1, 5)) / 10.0
        game.scoreA += 1
        game.updateStatus()
        turtle.update()
        time.sleep(0.3)

    # kolizja z lewym borderem
    if ball.xcor() <= -400:
        ball.goto(player.xcor() + 10 + 10 * ball.radius, player.ycor())
        ball.dx = 1.0
        if random.randint(1, 2) == 1:
            ball.dy = float(random.randint(1, 5)) / 10.0
        else:
            ball.dy = - float(random.randint(1, 5)) / 10.0
        game.scoreB += 1
        game.updateStatus()
        turtle.update()
        time.sleep(0.3)

    # warunek przegranej
    if game.scoreB >= game.goalScore:
        game.status = 'lost'
        game.updateStatus()
        if restart() == False:
            break
        else:
            continue

    # zmiany poziomow
    if game.scoreA >= game.goalScore and game.level == 1:
        game.level = 2
        game.scoreA = 0
        game.scoreB = 0
        game.updateStatus()
        player.length = 8
        player.shapesize(stretch_wid = 1.0, stretch_len = player.length, outline = None)
        player.boundary = 'none'
        print('Level: 2')

    if game.scoreA >= game.goalScore and game.level == 2:
        game.scoreA = 0
        game.scoreB = 0
        game.level = 3
        game.updateStatus()
        player.length = 6
        player.shapesize(stretch_wid = 1.0, stretch_len = player.length, outline = None)
        player.boundary = 'none'
        print('Level: 3')

    # warunek wygranej
    if game.scoreA >= game.goalScore and game.level == 3:
        game.status = 'win'
        game.updateStatus()
        if restart() == False:
            break
        else:
            continue

    # zwiekszenie szybkosci pilki i paletki przeciwnika
    if game.counter >= 300:
        game.counter = 0
        if ball.speed < 20:
            ball.speed += 4
            opponent.step += 6
            print('Ball\'s speed and opponent\'s step are boosted')
    
    # ruch paletki przeciwnika
    if opponent.boundary == 'bottom':
        opponent.up()

    if opponent.boundary == 'upper':
        opponent.down()
        