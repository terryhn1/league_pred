from math import exp
import pyGMs as gm
import numpy as np

"""
    Variables can use an average of training data to determine the states seen.

    Jungle Monsters Killed: 16 States(4-bit number indicating red/blue teamplay indicator + team lead diff)

    Turrets Destroyed: 4 States(max of 3 turrets can be destroyed early game if large teamplay)

    Total CS Difference: 2 States(average threshold)

    Ward Score Difference: 3 States(0 for no team advantage, 1 for blue team advantage, 2 for red team advantage)

    Elite Monsters: 3 States(max of 2 elite monsters can be taken within first 10 minutes practically)

    Gold Difference: 2 States(average threshold)

    Experience Difference: 2 states(average threshold)

    Teamplay: 4 States(Based off a Teamplay Score Rating)

    Lane Dominance: 4 States(Based off a Lane Dominance Rating)

    KDA: 2 States(Average KDA)

    Win Condition: 2 states(Win or Lose)
"""
def initializeGraphModel():

    #Initialize the Variables
    jgMonstersKilled = gm.Var(0, 16)
    turretsDestroyed = gm.Var(1, 3)
    csDifference = gm.Var(2, 3)
    wardScoreDifference = gm.Var(3, 3)
    eliteMonsters = gm.Var(4, 3)
    goldDifference = gm.Var(5, 3)
    expDifference = gm.Var(6, 3)
    avgKDA = gm.Var(7, 3)
    laneDominance = gm.Var(8, 3)
    teamplayScore = gm.Var(9, 3)
    winCondition = gm.Var(10, 2)

    #Initialize the factors

    f1 = gm.Factor([jgMonstersKilled])
    f2 = gm.Factor([turretsDestroyed])
    f3 = gm.Factor([csDifference])
    f4 = gm.Factor([wardScoreDifference])
    f5 = gm.Factor([eliteMonsters])
    f6 = gm.Factor([goldDifference, jgMonstersKilled, csDifference, eliteMonsters])
    f7 = gm.Factor([expDifference, jgMonstersKilled, csDifference])
    f8 = gm.Factor([avgKDA])
    f9 = gm.Factor([laneDominance, goldDifference, expDifference, avgKDA])
    f10 = gm.Factor([teamplayScore, jgMonstersKilled, turretsDestroyed, wardScoreDifference, eliteMonsters])
    f11 = gm.Factor([winCondition, laneDominance, teamplayScore])

    factors = [f1,f2, f3, f4, f5, f6, f7, f8, f9, f10, f11]

    return gm.GraphModel(factors), factors

def loadData(model,factors):
    data = np.genfromtxt("data.csv", delimiter = ",")
    data_int = np.array([list(xj) for xj in data],dtype= int)
    nTrain = int(.75 * len(data_int))   
    train = data_int[:nTrain]
    valid = data_int[nTrain:]


    jgMonstersKilled = model.X[0]; turretsDestroyed = model.X[1]; csDifference = model.X[2]
    wardScoreDifference = model.X[3]; eliteMonsters = model.X[4]; goldDifference = model.X[5]
    expDifference = model.X[6]; avgKDA = model.X[7]; laneDominance = model.X[8]
    teamplayScore = model.X[9]; winCondition = model.X[10]

    # Maximum Likelihood Estimator
    for xj in train:
        factors[0][xj[jgMonstersKilled]] += 1.0
        factors[1][xj[turretsDestroyed]] += 1.0
        factors[2][xj[csDifference]] += 1.0
        factors[3][xj[wardScoreDifference]] += 1.0
        factors[4][xj[eliteMonsters]] += 1.0
        factors[5][xj[jgMonstersKilled], xj[csDifference], xj[eliteMonsters], xj[goldDifference]] += 1.0
        factors[6][xj[jgMonstersKilled], xj[csDifference], xj[expDifference]] += 1.0
        factors[7][xj[avgKDA]] += 1.0
        factors[8][xj[goldDifference], xj[expDifference], xj[avgKDA], xj[laneDominance]] += 1.0
        factors[9][xj[jgMonstersKilled], xj[turretsDestroyed], xj[csDifference], xj[eliteMonsters], xj[teamplayScore]] += 1.0
        factors[10][xj[laneDominance], xj[teamplayScore], xj[winCondition]] += 1.0

    for i in range(len(model.factors)):
        factors[i] /= len(train)
    
    return gm.GraphModel(factors), valid




