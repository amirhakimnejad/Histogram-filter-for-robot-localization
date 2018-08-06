'''
    File name: 2DHistogramLocalization.py
    Author: <a href="mailto:a.hakimnejad@mrl-spl.ir">Amirhossein Hakimnejad</a>
    Date created: August 4, 2018
    Date last modified: August 7, 2018
    Python Version: 3.x
'''

# sensorTrust is the sensors trustworthiness. It is it's probability of being right about what it sees
# actionTrust is how much the robot is sure about his movement in the right direction
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
        for row in range(len(p)):
            for col in range(len(p[row])):
                if measurement == field[row][col]:
                    q.append(p[row][col] * trust)
                else:
                    q.append(p[row][col] * (1 - trust))

        s = sum(q)
        q = normalizer(q, s, len(p[0]))
        return q

    p = move(p, motion, actionTrust)
    p = sense(p, measurement, sensorTrust)
    return p

# W: robot senses white color
# B: robot senses black color
field = [['W','B','B','W','W'],
          ['W','W','B','W','W'],
          ['W','W','B','B','W'],
          ['W','W','W','W','W']]

# p is the uniform distribution that the robot has no idea where it is at first
pinit = 1.0 / float(len(field)) / float(len(field[0]))
p = [[pinit for row in range(len(field[0]))] for col in range(len(field))]

# In this example, first the robot moves, then it senses and it sees the color of where it standing
# Motion help
# [0,0] - stay
# [0,1] - move to right
# [0,-1] - move to left
# [1,0] - move down
# [-1,0] - move up
motions = [[0,0],[0,1],[1,0],[1,0],[0,1]]
measurements = ['B','B','B','B','B']

for i in range(len(motions)):
    p = localize(p, field, measurements[i], motions[i], sensorTrust = 0.7, actionTrust = 0.8)

# displays final distribution
def show(p):
    rows = ['[' + ','.join(map(lambda x: '{0:.5f}'.format(x),r)) + ']' for r in p]
    print ('[' + ',\n '.join(rows) + ']')

show(p)
