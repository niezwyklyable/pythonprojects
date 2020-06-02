
import turtle

class Game():
    def __init__(self):
        self.penStatus = turtle.Turtle()
        self.penStatus.color('white')
        self.penStatus.ht()
        self.penStatus.penup()
        self.penStatus.goto(-390, 160)
        self.level = 1
        self.score = 0
        self.cities = 6
        self.silos = 3
        self.playerMissiles = 30
        self.enemyMissiles = 1
        # zmienne, lista i flaga potrzebne do trigerowania funkcji launchEnemyMissile()
        # z opoznieniem czasowym
        self.counter = 0 
        self.missileLaunched = 0
        self.randTime = [] 
        self.nextLevel = False

    def updateStatus(self):
        self.penStatus.clear()
        msg = 'Missile Command\n' \
              'Level: ' + str(self.level) + '\n' \
              'Score: ' + str(self.score) + '\n' \
              'Cities: ' + str(self.cities) + '\n' \
              'Silos: ' + str(self.silos) + '\n' \
              'Player Missiles: ' + str(self.playerMissiles) + '\n' \
              'Enemy Missiles: ' + str(self.enemyMissiles)
        self.penStatus.write(msg, font=('Arial', 12, 'normal'))

    def viewSummary(self):
        print('Level ' + str(self.level) + ' completed.')
        print('City bonus: ' + str(self.cities * 100) + ' Silo bonus: ' + str(self.silos * 50) \
            + ' Missile bonus: ' + str((self.playerMissiles + self.level) * 10))
        self.score += self.cities * 100 + self.silos * 50 + \
            (self.playerMissiles + self.level) * 10
