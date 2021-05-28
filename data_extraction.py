import numpy as np

"""
Game Data Organization
-----------------------
Data only includes the first 10 minutes of each game

Index 0: Unique Game ID
Index 1: Win Condition(1 for Blue, 0 for Red)
Index 2-20: Blue Data
Index 21 -39: Red Data

Team Data Split:
    Index 0: Wards Placed
    Index 1: Enemy Wards Destroyed
    Index 2: First Blood(0 or 1)
    Index 3: Team Kills
    Index 4: Team Deaths
    Index 5: Team Assists
    Index 6: Dragons, Heralds Taken
    Index 7: Dragons Taken
    Index 8: Heralds Taken
    Index 9: Enemy Turrets Killed
    Index 10: Total Gold
    Index 11: Average Level of Champions
    Index 12: Total Experience
    Index 13: Total CS
    Index 14: Total Jungle Monsters Killed
    Index 15: Gold Difference(can be negative)
    Index 16: Experience Difference(can be negative)
    Index 17: CS/Min
    Index 18: Gold/Min
"""

#Functions for N x 19 Arrays
def getWardData(team_data):
    return team_data[:,0:2]

def getFirstBlood(team_data):
    return team_data[:,1]

def getTeamKDA(team_data):
    return team_data[:,3:6]

def getObjectives(team_data):
    return team_data[:,6:10]

def getTotalStats(team_data):
    return team_data[:,10:15]

def getGoldEXPDifference(team_data):
    return team_data[:,15:17]

def getFarmPerMin(team_data):
    return team_data[:,17:19]

if __name__ == "__main__":

    #Load in league data. File name can vary
    data = np.genfromtxt("diamond_data.csv", delimiter = ",")[1:]

    #Separation of Data
    win_condition = data[:,1]
    blue_data = data[:,2:21]
    red_data = data[:,21:40]


    #FILL IN FOR DATA VIEW

