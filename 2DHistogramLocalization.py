'''
    File name: fieldMaker.py
    Author: <a href="mailto:a.hakimnejad@mrl-spl.ir">Amirhossein Hakimnejad</a>
    Date created: August 4, 2018
    Date last modified: August 10, 2018
    Python Version: 3.x
'''
# TODO: The field distribution is still cicular
# TODO: Get max item of distribution and show it in the field in another color
# TODO: If input was empty for 0.7 of a second or 1, consider it as a stand frame for the robot

import sys, termios, tty, os, time
from random import randint

# Everything you need to edit is here
# Field length
A = 100
# Field width
B = 50
# Penalty area length
E = 18
# Penalty area width
F = 44
# Penalty cross distance
G = 12
# Center circle diameter
H = 15

# realRobotPose is where the robot really is(the red block in terminal) but it does'nt know.
# So the measurement is based on this position of the field.
# The robot thinks he is somewhere else but what he sees is matching with the realRobotPose environment.
# So it tries to localize itself based on this.
realRobotPose = [29, 30]

# measurement is a square matrix of what the robot sees
measurementLength = 13

# Motion help
# [0,0] - stay
# [0,1] - move to right
# [0,-1] - move to left
# [1,0] - move down
# [-1,0] - move up


# sensorTrust is the sensors trustworthiness. It is it's probability of being right about what it sees.
# actionTrust is how much the robot is sure about his movement in the right direction
sensorTrust = 0.7
actionTrust = 0.6

# robotField is a two dimensional matrix of what he knows about the real field.
# it's kind of a map of the empty field that he use to compare its measurments with is.

# inputLuck is the percentage of the luck that input work or not. That means you may press 'd' for example but the robot stays where it was beforeself.
# It is seperate from motion or measurement trust. Its more like a noise.
inputLuck = 80

# 'W': robot senses white color, he sees line in this problem
# 'B': robot senses black color, anything except lines is black for the robot
def draw(i, j, A, B, E, F, G, H, realRobotPose, fieldRow, visual):

    def isEdge(i, j, B, A):
        return i == 0 or i == B - 1 or j == 0 or j == A - 1

    def isMidLine(j, A):
        return j == int(round(A / 2))

    def isLeftPenaltyBox(i, j, B, E, F):
        lefBoxVerticLine = j == E - 1 and i > ((B - F) / 2)  and i < (B - F) / 2 + F - 1
        lefBoxHorizLine =  j < E and (i == int(round((B - F) / 2)) or i == int(round((B - F) / 2 + F) - 1))
        return lefBoxVerticLine or lefBoxHorizLine

    def isRightPenaltyBox(i, j, A, B, E, F):
        rightBoxVerticLine = j == A - E and i > (B - F) / 2 and i < (B - F) / 2 + F - 1
        rightBoxHorizLine = j >= A - E and (i == int(round((B - F) / 2)) or i == int(round((B - F) / 2 + F - 1)))
        return rightBoxVerticLine or rightBoxHorizLine

    def isPenaltySpot(i, j, A, B, G):
        leftPenaltySpot = j == G - 1 and i == int(round(B / 2 - 1))
        rightPenaltySpot = j == A - G and i == int(round(B / 2 - 1))
        return leftPenaltySpot or rightPenaltySpot

    def isCircle(i, j, A, B, H):
        mid = [A / 2, B / 2 - 1]
        return int(round(H/2)) == int(round(((j - mid[0])**2 + (i - mid[1])**2)**0.5))

    def isCenterSpot(i, j, A, B):
        mid = [A / 2, B / 2 - 1]
        return i == mid[1] and (j == mid[0] - 1 or j == mid[0] + 1)

    if visual == True:
        if i == realRobotPose[0] and j == realRobotPose[1]:
            print ('\033[101m  ', end='')
        elif isEdge(i, j, B, A) or isMidLine(j, A) or isLeftPenaltyBox(i, j, B, E, F) or isRightPenaltyBox(i, j, A, B, E, F) or isPenaltySpot(i, j, A, B, G) or isCircle(i, j, A, B, H) or isCenterSpot(i, j, A, B):
            print ('\033[107m  ', end='')
        else:
            print ('\033[42m  ', end='')
    else:
        if isEdge(i, j, B, A) or isMidLine(j, A) or isLeftPenaltyBox(i, j, B, E, F) or isRightPenaltyBox(i, j, A, B, E, F) or isPenaltySpot(i, j, A, B, G) or isCircle(i, j, A, B, H) or isCenterSpot(i, j, A, B):
            fieldRow.append('W')
        else:
            fieldRow.append('B')

def drawer(A, B, E, F, G, H, realRobotPose, visual):
    field = []
    fieldRow = []
    for i in range(B):
        for j in range(A):
            draw(i, j, A, B, E, F, G, H, realRobotPose, fieldRow, visual)
        if visual == True:
            print ('\033[0m\n', end='')
        else:
            field.append(fieldRow)
            fieldRow = []

    return field

class _Getch:
    def __call__(self):
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(3)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

def robotMover(i, j, realRobotPose, kidnapped = False):
    clear = lambda: os.system('clear')
    clear()
    if not kidnapped:
        realRobotPose[0] += i
        realRobotPose[1] += j
    else:
        realRobotPose[0] = i
        realRobotPose[1] = j
    drawer(A, B, E, F, G, H, realRobotPose, True)

def localize(p, field, measurement, motion, sensorTrust, actionTrust):

    def normalizer(q, sum, colsNumber):
        normalized = []
        row = []
        for i in range(len(q)):
            q[i] = q[i] / sum
            row.append(q[i])
            if (i + 1) % (colsNumber) == 0:
                normalized.append(row)
                row = []
        return normalized

    def move(p, motion, trust):
        q = []
        for row in range(len(p)):
            for col in range(len(p[row])):
                s = p[(row - motion[0])% len(p)][(col-motion[1])% len(p[row])] * trust
                s += p[row % len(p)][col % len(p[row])] * (1 - trust)
                q.append(s)

        s = sum(q)
        q = normalizer(q, s, len(p[0]))
        return q

    def sense(p, measurement, trust):
        q = []
        def xor(measurement, field, pZGivenX, fieldRow, fieldCol):
            outValue = 'B'
            for row in range(len(measurement)):
                for col in range(len(measurement[0])):
                    outSenario = (row - int(len(measurement)/2)) + fieldRow < 0 or (col - int(len(measurement[0])/2)) + fieldCol < 0 or (row - int(len(measurement)/2)) + fieldRow >= B or (col - int(len(measurement[0])/2)) + fieldCol >= A
                    if outSenario:
                        if measurement[row][col] == outValue:
                            pZGivenX *= trust
                        else:
                            pZGivenX *= (1 - trust)

                    elif measurement[row][col] == field[fieldRow + row - int(len(measurement)/2)][fieldCol + col - int(len(measurement[0])/2)]:
                        pZGivenX *= trust
                    else:
                        pZGivenX *= (1 - trust)

            return pZGivenX

        for row in range(len(p)):
            for col in range(len(p[0])):
                pZGivenX = xor(measurement, robotField, 1, row, col)
                q.append(p[row][col] * pZGivenX)

        s = sum(q)
        q = normalizer(q, s, len(p[0]))
        return q

    p = move(p, motion, actionTrust)
    p = sense(p, measurement, sensorTrust)
    return p

def printt(p):
    print()
    for i in range(len(p)):
        for j in range(len(p[0])):
            print('   '+str(p[i][j]) + '  ', end='')
        print()

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)

    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def saveToFile(p):
    rows = [','.join(map(lambda x: '{0:.5f}'.format(x),r)) for r in p]
    csv = '\n '.join(rows)
    with open('distribution.csv', 'w') as f:
        f.write(csv)

def play(p, realRobotPose, measurementLength, inputLuck, sensorTrust, actionTrust):
    saveToFile(p)
    while True:
        i = 0
        j = 0
        kidnapped = False
        char = getch()
        motion = [0, 0]
        if (char == "q"):
            break

        if (char == "a"):
            j -= 1

        elif (char == "d"):
            j += 1

        elif (char == "w"):
            i -= 1

        elif (char == "s"):

            i += 1

        elif (char == "k"):
            kidnapped = True

        motion = [i, j]
        if randint(0, 100) > inputLuck:
            i = 0
            j = 0


        if kidnapped:
            robotMover(randint(0, B - 1), randint(0, A - 1), realRobotPose, kidnapped)
        else:
            robotMover(i, j, realRobotPose, kidnapped)

        measurementRow = []
        measurement = []
        for x in range(int(measurementLength/2*-1), int(measurementLength/2) + 1):
            for y in range(int(measurementLength/2*-1), int(measurementLength/2) + 1):
                if realRobotPose[0] + x < 0 or realRobotPose[1] + y < 0 or realRobotPose[0] + x >= len(robotField) or realRobotPose[1] + y >= len(robotField[0]):
                    measurementRow.append('B')
                    print ('\033[42m   ', end='')

                else:
                    measurementRow.append(robotField[realRobotPose[0] + x][realRobotPose[1] + y])
                    if x == 0 and y == 0:
                        print ('\033[101m   ', end='')
                    elif robotField[realRobotPose[0] + x][realRobotPose[1] + y] == 'B':
                        print ('\033[42m   ', end='')
                    else:
                        print ('\033[107m   ', end='')

            print()
            measurement.append(measurementRow)
            measurementRow = []

        print ('\033[0m\n\n', end='')
        p = localize(p, robotField, measurement, motion ,sensorTrust, actionTrust)
        saveToFile(p)
        # displays final distribution

robotField = []
# p is the uniform distribution that the robot has no idea where it is at first
pinit = 1.0 / float(B / float(A))
p = [[pinit for row in range(A)] for col in range(B)]

# Draw the first version of the field with our robot in his place at it's set state
drawer(A, B, E, F, G, H, realRobotPose, True)
robotField = drawer(A, B, E, F, G, H, realRobotPose, False)

# Let's play
play(p, realRobotPose, measurementLength, inputLuck, sensorTrust, actionTrust)
