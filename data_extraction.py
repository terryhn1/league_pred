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

#Create the simple Functions for N x 19 Arrays to extract individual data
def getWardData(team_data):
    return team_data[:,0:2]

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

#simple functions
def _simple3(diff, data):
    for i in range(len(diff)):
        if diff[i] == 0: data[i] = 0
        elif diff[i] > 0: data[i] = 1
        elif diff[i] < 0: data[i] = 2
    return data


#Scoring
def setWardStates(blue_data, red_data):
    blueWardData = getWardData(blue_data)
    redWardData = getWardData(red_data)
    wardDifference = np.sum(blueWardData, axis =1) - np.sum(redWardData,axis = 1)
    data = np.zeros(wardDifference.shape)
    for i in range(len(wardDifference)):
        if wardDifference[i] == 0: data[i] = 0
        elif wardDifference[i] > 0: data[i] = 1
        elif wardDifference[i] < 0: data[i] = 2
    
    return data

def setJGMonstersKilled(blue_data, red_data):
    blueJG = getTotalStats(blue_data)[:,-1]
    redJG = getTotalStats(red_data)[:,-1]

    #Put it into thresholds
    avgJG = np.sum(blueJG) + np.sum(redJG) / (len(blueJG) * 2)
    minJG = min(blueJG) if min(blueJG) < min(redJG) else min(redJG)
    maxJG = max(blueJG) if max(blueJG) > max(redJG) else max(redJG)

    #meet at midpoint for the threshold for now
    leftthres = (avgJG + minJG) / 2.0 
    rightthres = (avgJG + maxJG) / 2.0

    #data separation
    data = np.zeros(blueJG.shape)

    #Identify whether Junglers show Gold Dominance, Experience Difference, or Teamplay
    #All values are written in binary to cover a 4-bit number

    for i in range(len(data)):
        blueTeamplayOriented = 1 if leftthres < blueJG[i] <= rightthres else 0
        redTeamplayOriented = 1 if leftthres < redJG[i] <= rightthres else 0

        jgKillsDifference = blueJG[i] - redJG[i]
        blueLead = 1 if jgKillsDifference >  0 else 0
        redLead = 1 if jgKillsDifference < 0 else 0

        data[i] = int(str(blueTeamplayOriented) + str(blueLead) + str(redTeamplayOriented) + str(redLead), 2)
    
    return data

def setTurretsDestroyed(blue_data, red_data):
    blueTurretScore = getObjectives(blue_data)[:,-1]
    redTurretScore = getObjectives(red_data)[:,-1]
    diff = blueTurretScore - redTurretScore

    data = np.zeros(blueTurretScore.shape)

    #We are interested in seeing which team displays more teamplay
    #Therefore the states that given are only 0, 1, and 2
    return _simple3(diff, data)

def setCSDifference(blue_data, red_data):
    blueMinionScore = getTotalStats(blue_data)[:,3]
    redMinionScore = getTotalStats(red_data)[:,3]
    diff = blueMinionScore - redMinionScore
    data = np.zeros(blueMinionScore.shape)

    #Minions killed is a sign of lane dominance need to expend 0,1,2 as the states 
    # 0: indicates theres probably no difference in win condition
    # 1: indicates blue team is more preferred
    # 2: indicates red team is more preferred

    return _simple3(diff, data)

def setEliteMonsters(blue_data, red_data):
    #There is a max of two elites that can be taken. They are good indicators of gold
    #and teamplay throughout the match. WE take on the same structure as previous methods
    blueElites = getObjectives(blue_data)[:,0]
    redElites = getObjectives(red_data)[:,0]
    diff = blueElites - redElites
    data = np.zeros(blueElites.shape)

    return _simple3(diff,data)

def setGoldDifference(blue_data):
    #3 Possible states
    #TODO Weight out the difference to take out small differences(Not good indicator of a win condition)
    blueGoldDiff = getGoldEXPDifference(blue_data)[:,0]
    data = np.zeros(blueGoldDiff.shape)

    return _simple3(blueGoldDiff, data)

def setExperienceDifference(blue_data):
    #TODO Weight out the difference to take out small differences(Not good indicator of win condition)
    blueEXPDiff = getGoldEXPDifference(blue_data)[:,-1]
    data = np.zeros(blueEXPDiff.shape)

    return _simple3(blueEXPDiff, data)

def setKDADifference(blue_data, red_data):

    #TODO Weight out the difference to take out small differences(Not good indicator of )
    blueKDA = getTeamKDA(blue_data)
    redKDA = getTeamKDA(red_data)

    #Normalize KDA
    blueKDA = (blueKDA[:,0] + blueKDA[:,2]) / (blueKDA[:,1] + 1)
    redKDA = (redKDA[:,0] + redKDA[:,2]) / (redKDA[:,1] + 1)

    diff = blueKDA - redKDA
    data = np.zeros(blueKDA.shape)

    return _simple3(diff,data)

def laneScoring(team_data, win_condition, team):
    #The higher the gold, then possibility of better items(more control of the game)
    #the higher the exp, then the possibility of reaching skill ranks faster to make a difference
    gold = getTotalStats(team_data)[:,0]
    exp = getTotalStats(team_data)[:,1]
    kda = getTeamKDA(team_data)
    kda = (kda[:,0] + kda[:,2]) / (kda[:,1] + 1)

    if team == "b":
        goldThresh = gold * win_condition
        expThresh = exp * win_condition
        kdaThresh = kda * win_condition
    elif team == "r":
        goldThresh = gold * np.logical_not(win_condition)
        expThresh = exp * np.logical_not(win_condition)
        kdaThresh = kda * np.logical_not(win_condition)

    #Confidence level of 10%

    goldIndices, = np.where(goldThresh == 0)
    goldWinThresh = np.mean(np.delete(goldThresh, goldIndices)) * 0.9
    expIndices, = np.where(expThresh == 0)
    expWinThresh = np.mean(np.delete(expThresh, expIndices)) * 0.96
    kdaIndices, = np.where(kdaThresh == 0)
    kdaWinThresh = np.mean(np.delete(kdaThresh, kdaIndices)) * 0.4

    goldScoring = np.zeros(goldThresh.shape); expScoring = np.zeros(expThresh.shape); kdaScoring = np.zeros(kda.shape)
    for i in range(len(goldScoring)):
        if gold[i] < goldWinThresh: goldScoring[i] = 1.5
        else: goldScoring[i] = 0.5
        if exp[i] < expWinThresh: expScoring[i] = 1.5
        else: expScoring[i] = 0.5
        if kda[i] < kdaWinThresh: kdaScoring[i] = 1.5
        else: kdaScoring[i] = 0.5
    
    return goldScoring + expScoring + kdaScoring

def setLaneTeamplayDifference(blueScore, redScore):
    diff = blueScore - redScore
    data = np.zeros(diff.shape)
    
    return _simple3(diff, data)

def teamplayScoring(team_data,win_condition, team):
    #find a good weight for jungle monsters, turrets, ward score, elite monsters
    jungleMonsters = getTotalStats(team_data)[:,-1]
    turrets = getObjectives(team_data)[:,-1]
    wardScore = np.sum(getWardData(team_data), axis = 1)
    eliteMonsters = getObjectives(team_data)[:,0]

    #outweigh the elite Monsters and turrets(more significant in the first 10 mins as an indicator)
    turretScoring = turrets * 10
    eliteScoring  = eliteMonsters * 10

    #Reduce the scoring of the wards(more wards the better)
    wardScoring = wardScore / 5.0

    #jungleMonsters: bad teamplay if very low
    # good teamplay if decently average
    # but can be indicator of jungle solo play if too high
    if team == "b":
        thres = jungleMonsters * win_condition
    elif team == "r":
        thres = jungleMonsters * np.logical_not(win_condition)
    
    indices = np.where(thres == 0)
    right_thres = np.mean(np.delete(thres, indices)) * 1.3
    left_thres = np.mean(np.delete(thres, indices)) * 0.7

    jungleScoring = np.zeros(jungleMonsters.shape)

    for i in range(len(jungleScoring)):
        if jungleMonsters[i] < left_thres: jungleScoring[i] = jungleMonsters[i] / 10.0
        elif jungleMonsters[i] < right_thres: jungleScoring[i] = jungleMonsters[i] / 5.0
        else: jungleScoring[i] = jungleMonsters[i] / 8.0

    return turretScoring + jungleScoring + wardScoring + eliteScoring

#Creating new data that uses the average data: KDA, Jungle Monsters Killed, CS Difference, Ward Score Diff, Gold Diff, Exp Diff, 
#Reordering into the following topographic order: Jungle Monsters, Turrets Destroyed, Total CS Diff, Ward Score, Elite Monsters, Gold Diff, Experience Diff, KDA, Lane Dominance, Teamplay, Win Condition
def dataSetTrueExtraction():

    #Load in league data. File name can vary
    data = np.genfromtxt("diamond_data.csv", delimiter = ",")[1:]

    #Separation of Data
    win_condition = data[:,1]
    blue_data = data[:,2:21]
    red_data = data[:,21:40]

    #Independent Factors for the new data set
    wardDifference = setWardStates(blue_data, red_data)
    jungleDifference = setJGMonstersKilled(blue_data, red_data)
    turretsDifference = setTurretsDestroyed(blue_data, red_data)
    CSDifference = setCSDifference(blue_data, red_data)
    eliteMonstersDifference = setEliteMonsters(blue_data, red_data)

    #Dependent Factors for the new data set
    goldDifference = setGoldDifference(blue_data)
    expDifference = setExperienceDifference(blue_data)
    kdaDifference = setKDADifference(blue_data,red_data)

    #Factors that require scoring based
    #Lane Dominance: Can estimate this through Gold Difference, Experience, and KDA
    #Teamplay: Can estimate this through Jungle Monsters Killed, Turrets Destroyed, Ward Score, and Elite Monsters killed.
    blueTeamplayScore = teamplayScoring(blue_data, win_condition, "b")
    redTeamplayScore = teamplayScoring(red_data,win_condition, "r")
    teamplayDifference = setLaneTeamplayDifference(blueTeamplayScore, redTeamplayScore)

    blueLaneScore = laneScoring(blue_data, win_condition, "b")
    redlaneScore = laneScoring(red_data, win_condition, "r")
    laneDifference = setLaneTeamplayDifference(blueLaneScore, redlaneScore)

    scores = np.array([jungleDifference, turretsDifference, CSDifference, wardDifference, eliteMonstersDifference,
                        goldDifference, expDifference, kdaDifference, laneDifference, teamplayDifference, win_condition]).T

    return scores

if __name__ == "__main__":
    data = dataSetTrueExtraction()
    np.savetxt("data.csv", data, delimiter = ",")

