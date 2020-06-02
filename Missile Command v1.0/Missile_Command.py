
import turtle
import time
import random

turtle.bgcolor('black')
turtle.ht()
turtle.setup(800, 600)
turtle.title('Missile Command by AW v1.0')
turtle.tracer(0)

from game import Game
from sprites import City
from sprites import Silo
from sprites import Center
from sprites import PlayerMissile
from sprites import EnemyMissile

game = Game()

cities = []
posX = [] # przechowuje potencjalne miejsca wystrzelenia pocisku wroga
for i in range(6):
    x = -250 + i * 100
    y = -250
    cities.append(City(x, y, 'green', 'square'))
    posX.append(x)

silos = []
centers = []
for i in range(3):
    x = -350 + i * 350
    y = -225
    silos.append(Silo(x, y, 'blue', 'square'))
    centers.append(Center(x, y, 'white', 'circle'))
    posX.append(x)

targets = cities + silos # przekopiowanie obiektow do jednej listy 
# (usuniecie obiektu w jednej z tych dwoch list nie spowoduje usuniecia obiektu w liscie 
# laczacej targets)

enemyMissiles = []
playerMissiles = []

def launchPlayerMissile(x, y):
    if game.playerMissiles > 0:
        game.playerMissiles -= 1
        if x < -175:
            startX = -350
        elif x > 175:
            startX = 350
        else:
            startX = 0
        playerMissiles.append(PlayerMissile(startX, -225, 'white', 'circle', x, y))

def click(x, y):
        print(str(x) + ', ' + str(y))

def launchEnemyMissile():
    randTarget = random.randint(0, len(targets) - 1)
    enemyMissiles.append(EnemyMissile(posX[random.randint(0, 8)], 400, \
    'red', 'circle', targets[randTarget].xcor(), targets[randTarget].ycor()))

launchEnemyMissile() # wystrzelenie pierwszego pocisku wroga (level 1)

# nasluch myszki
#turtle.listen() # to jest tylko do keyboarda
turtle.onscreenclick(launchPlayerMissile, 1) # 1 (default) - LMB, 3 - RMB
turtle.onscreenclick(click, 3) # to jest zawsze przydatne nawet gdy nie korzystamy z myszki

while True:

    # render
    game.updateStatus()
    turtle.update()
    time.sleep(0.02)

    for em in enemyMissiles:

        # fizyka pocisku gracza
        if em.status == 'normal':
            em.move()
        if em.status == 'end':
            em.clear()
            em.ht()
            enemyMissiles.remove(em)
        if em.status == 'explode' or em.status == 'fadeOut':
            em.explosion()

        # kolizja pocisku gracza z miastami
        for c in cities:
            if em.isCollision(c):
                em.status = 'explode'
                # usuniecie celu z listy celow
                for t in targets:
                    if t.xcor() == c.xcor():
                        targets.remove(t)
                c.ht()
                cities.remove(c)
                game.cities -= 1
                game.enemyMissiles -= 1

        # kolizja pocisku gracza z silosami
        for s in silos:
            if em.isCollision(s):
                em.status = 'explode'
                # usuniecie celu z listy celow
                for t in targets:
                    if t.xcor() == s.xcor():
                        targets.remove(t)
                s.ht()
                silos.remove(s)
                game.silos -= 1
                game.enemyMissiles -= 1

        # wyjscie pocisku gracza poza mape
        if em.ycor() <= -260 and em.status == 'normal':
            em.status = 'explode'
            game.enemyMissiles -= 1
    
    for pm in playerMissiles:
        # fizyka pocisku gracza
        if pm.status == 'normal':
            pm.move()
        if pm.status == 'end':
            pm.clear()
            pm.ht()
            playerMissiles.remove(pm)
        if pm.status == 'explode' or pm.status == 'fadeOut':
            pm.explosion()
            # kolizja pocisku gracza z pociskami wroga
            for em in enemyMissiles:
                if pm.isCollision(em) and em.status == 'normal':
                    em.status = 'end'
                    game.enemyMissiles -= 1

    # warunek konca gry (albo nie bedzie czego bronic albo nie bedzie sie czym bronic)
    if game.cities <= 0 or game.silos <= 0:
        print('Gave over! Score: ' + str(game.score))
        break

    # nastepny level
    if  game.enemyMissiles <= 0:
        game.viewSummary()
        game.level += 1
        game.enemyMissiles = game.level
        if game.silos == 3:
            game.playerMissiles = 30
        elif game.silos == 2:
            game.playerMissiles = 20
        else:
            game.playerMissiles = 10
        game.nextLevel = True
        game.missileLaunched = 0
        game.counter = 0
        game.randTime = []
        for i in range(game.enemyMissiles):
             game.randTime.append(random.randint(0, 50)) # odstep czasowy = 20ms * arg
        
    # wystrzelenie pocisku wroga z opoznieniem
    if game.nextLevel:
        game.counter += 1
        if game.counter >= game.randTime[game.missileLaunched]:
            game.missileLaunched += 1
            if game.missileLaunched < game.level:
                launchEnemyMissile()
                game.counter = 0
            else:
                # wystrzelenie ostatniego pocisku
                launchEnemyMissile()
                game.nextLevel = False

input('Press enter to exit.')
