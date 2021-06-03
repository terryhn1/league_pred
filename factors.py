import pyGMs as gm
import numpy as np

"""
    Variables can use an average of training data to determine the states seen.

    Jungle Monsters Killed: 2 States(average threshold)

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
    jgMonstersKilled = gm.Var(0, 2)
    turretsDestroyed = gm.Var(1, 4)
    csDifference = gm.Var(2, 3)
    wardScoreDifference = gm.Var(3, 2)
    eliteMonsters = gm.Var(4, 3)
    goldDifference = gm.Var(5, 2)
    expDifference = gm.Var(6, 2)
    teamplayScore = gm.Var(7, 4)
    avgKDA = gm.Var(8,2)
    laneDominance = gm.Var(9,4)
    winCondition = gm.Var(10, 2)

    #Initialize the factors

    #Indepedent factors first
    f1 = gm.Factor([jgMonstersKilled])
    f2 = gm.Factor([turretsDestroyed])
    f3 = gm.Factor([csDifference])
    f4 = gm.Factor([wardScoreDifference])
    f5 = gm.Factor([eliteMonsters])


    #Dependent Factors after
    f6 = gm.Factor([goldDifference, jgMonstersKilled, jgMonstersKilled])
    f7 = gm.Factor([expDifference, jgMonstersKilled, csDifference])
    f8 = gm.Factor([teamplayScore, jgMonstersKilled, turretsDestroyed, wardScoreDifference, eliteMonsters])
    f9 = gm.Factor([laneDominance, goldDifference, expDifference, avgKDA])
    f10 = gm.Factor([winCondition, laneDominance, teamplayScore])

    return gm.GraphModel([f1,f2, f3, f4, f5, f6, f7, f8, f9, f10])



