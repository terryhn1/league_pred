import numpy as np

"""
The goal of this module is to estimate the relationship between certain pieces of data on winrate.
Common Structure: How does this stat relate to the win condition? What is the threshold for winning?
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


