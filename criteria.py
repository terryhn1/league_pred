import numpy as np

"""
The goal of this module is to estimate the relationship between certain pieces of data on winrate.
Common Structure: How does this stat relate to the win condition? What is the threshold for winning?

Common Criteria:
    First 10 Minutes of every game is mainly the Laning Phase. Therefore, we should look at whether a team is dominating their lanes overall.
    Throughout the game, different factors from the data collected can showcase teamplay difference.

    Negative values correlates with lower chance of winning(The effect of snowballing)

    More wards placed correlates with more teamplay(chances of seeing Herald or Dragon done increases)
        - Similarly, wards destroyed means better defense
        - Warding difference in placed/destroyed needs to be evaluated

    Early Game CS score correlates to lane dominance

    First Blood is open-ended in higher tier play, but can be taken into consideration
        - First blood is dependent on teamplay or lane dominance
            -Lane dominance determined by Ward Control, and CS difference

    Jungle Monsters Killed correlates to jungle dominance
        - If Jungler takes a lot of kills, then can assume "Farming" and is inactive in ganking
        - If Jungler takes an average amount of kills, then can assume jungler is active in ganking
        - If Jungler takes a low amount of kills, can assume that there is counter jungling and jungler is behind in gold overall
            - In this case, junglers at higher ELO may start to rely on ganking for money.
    
    If Experience is High, but Total Gold is low, then Lane dominance is bad overall
    
    If Experience is High as well as Total Gold, then snowballing effect can play into late game

    With the Turret Plating Update, taking down a turret in 10 minutes takes teamwork. Therefore, we can attribute turrets destroyed to teamplay/cooperation

    High cooperation in a team gives more advanced gameplay. Factors that determine teamwork can judge a game's outcome highly.



    Thus, we can separate into the certain dependent probabilities
        P(Teamplay | Jungle Monsters Killed), P(Lane Dominance | Wards Destroyed, Wards Placed)
        P(Lane Dominance | Total CS)
        P(Lane Dominance | Experience, Gold), P(Teamplay | Turrets Destroyed)
        P(Lane Dominance | )
        P(Win Condition | Teamplay, Lane Dominance)
    
    Lane Dominance and Teamplay are good indicators of a win condition for a team. Without lane dominance, then the Snowball Effect is not as prominent


"""


def goldDifferenceCriteria(data, win_condition):
    #Takes in N x 1 data(concerning gold difference) and N X 1 win_condition
    win_data = data * win_condition
    
    #Find average of the win_data
    avg_data = np.mean(win_data)

    #calculate for intervals
    left_interval = avg_data * .5
    right_interval = avg_data * 1.5


    #Find the indices of closely clustered data toward the middle using the average
    clustered = list()
    for i in range(len(win_data)):
        if win_data[i] >= left_interval and win_data[i] <= right_interval:
            clustered.append(i)
    
    clustered_win_data = np.array([win_data[i] for i in clustered])
    clustered_win_avg = np.mean(clustered_win_data)

    return clustered_win_data, clustered_win_avg

    #new_data


