
import turtle

class Game:
    
    def __init__(self, goalScore):

        # bordery
        self.border = turtle.Turtle()
        self.border.color('white')
        self.border.ht()
        self.border.penup()
        self.border.goto(-400, -300)
        self.border.pendown()
        self.border.pensize(3)
        for i in range(2):
            self.border.fd(800)
            self.border.lt(90)
            self.border.fd(600)
            self.border.lt(90)
        
        # status
        self.penStatus = turtle.Turtle()
        self.penStatus.color('white')
        self.penStatus.ht()
        self.penStatus.penup()
        self.penStatus.goto(-250, 310)
        self.scoreA = 0
        self.scoreB = 0
        self.level = 1
        self.status = 'playing'
        self.goalScore = goalScore
        self.counter = 0
        self.updateStatus()
        print('Level: 1')

        # opis sterowania
        self.controls = turtle.Turtle()
        self.controls.color('white')
        self.controls.ht()
        self.controls.penup()
        self.controls.goto(-320, -335)
        self.controls.write('Controls:    Up Arrow - Move Up/Stop,    Down Arrow - Move Down/Stop',\
            font=('Arial', 16, 'italic'))

    def updateStatus(self):
        self.penStatus.clear()
        if self.status == 'win': 
            msg = '                      You win!'
        elif self.status == 'lost':
            msg = '            Game over! You lost!'
        else:
            msg = 'Level: ' + str(self.level) + '      Player A: ' + str(self.scoreA) + \
                '      Player B: ' + str(self.scoreB)
        self.penStatus.write(msg, font=('Arial', 20, 'normal'))

    def restart(self):
        self.status = 'playing'
        self.level = 1
        self.scoreA = 0
        self.scoreB = 0
        self.updateStatus()
        self.counter = 0
        print('Level: 1')
