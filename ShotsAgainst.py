import matplotlib.pyplot as plt
from matplotlib.patches import Arc, Rectangle, ConnectionPatch
import pandas as pd
import statsbomb as sb
import ast
import econtools

def draw_goal(ax):
    goal_width = 8
    goal_height = 2.67
    goal_bottom_left = 36.0

    Goal = Rectangle((36,0), width=goal_width, height=goal_height, fill=False)
    element = [Goal]

    for i in element:
        ax.add_patch(i)

def get_team_number(name):
    switch = {
        'Washington Spirit': 759,
        'Seattle Reign': 760,
        'Chicago Red Stars': 761,
        'Houston Dash': 762,
        'Sky Blue FC': 763,
        'Orlando Pride': 764,
        'Portland Thorns': 765,
        'North Carolina Courage': 766,
        'Utah Royals': 767
    }
    return switch.get(name, None)

def get_team_name(number):
    switch = {
        759: 'Washington Spirit',
        760: 'Seattle Reign',
        761: 'Chicago Red Stars',
        762: 'Houston Dash',
        763: 'Sky Blue FC',
        764: 'Orlando Pride',
        765: 'Portland Thorns',
        766: 'North Carolina Courage',
        767: 'Utah Royals'
    }
    return switch.get(number, None)

def get_starting_lineups():
    return None

def get_shots_and_gks():
    '''Now Taken Care of in SB_GK_data.py'''
    return None

def what_zone(x,y):
    ## Check for valid x and y values
    zone = 0
    if x > 120 or x < 0:
        zone = 0
        return zone
    if y > 80 or y < 0:
        zone = 0
        return zone

    if x > 100:
        if y > 53.3:
            zone = 18
        elif y > 26.7:
            zone = 17
        elif y > 0:
            zone = 16
    elif x > 80:
        if y > 53.3:
            zone = 15
        elif y > 26.7:
            zone = 14
        elif y > 0:
            zone = 13
    elif x > 60:
        if y > 53.3:
            zone = 12
        elif y > 26.7:
            zone = 11
        elif y > 0:
            zone = 10
    elif x > 40:
        if y > 53.3:
            zone = 9
        elif y > 26.7:
            zone = 8
        elif y >= 0:
            zone = 7
    elif x > 20:
        if y > 53.3:
            zone = 6
        elif y > 26.7:
            zone = 5
        elif y >= 0:
            zone = 4
    else:
        if y > 53.3:
            zone = 3
        elif y > 26.7:
            zone = 2
        elif y >= 0:
            zone = 1

    return zone


def main(path='', date='', zones=None, teams=None):

    ### Load Data
    df_analysis = pd.read_csv('{0}{1}Shots_and_Keepers.csv'.format(path, date))

    # Some More DataFrames
    df_post = df_analysis.copy()  # Shots that hit the post
    df_on_target = df_analysis.copy()  # Shots on Target

    df_post = df_post[df_post['shot_outcome_name_shot'] == 'Post']
    df_on_target = df_on_target[df_on_target['shot_outcome_name_shot'].isin(shot_outcomes_on_target)]

    Goal = Rectangle((36, 0), width=goal_width, height=goal_height, fill=False)
    Post = Rectangle((35.67, 0), width=8.66, height=3, fill=False)

    ### Plot Set up
    fig = plt.figure()
    fig.set_size_inches(7, 5)
    goal_outline = fig.add_subplot(1, 1, 1)
    plt.ylim(-1, 4)
    plt.xlim(34, 46)
    plt.axis('off')

    ### Draw the Goal
    goal_outline.add_patch(Goal)
    goal_outline.add_patch(Post)

    goal_outline.scatter(df_on_target[df_on_target['possession_team'] == 'North Carolina Courage']['end_location_y'],
                         df_on_target[df_on_target['possession_team'] == 'North Carolina Courage']['end_location_z'],
                         c='green',
                         label='On Target', s=11, marker='o')
    print(df_analysis.head(15).to_string())
    plt.show()

field_end_x = 120.0
goal_width = 8
goal_height = 2.67
goal_bottom_left = 36.0

shot_outcomes = ['Saved', 'Blocked', 'Off T', 'Post', 'Goal', 'Wayward']
shot_outcomes_on_target = ['Saved', 'Post', 'Goal']
shot_outcomes_off_target = ['Off T', 'Wayward']

date_of_file= '200526'
date_of_file= '200605'
sb_path = 'C:\\Users\\JaysC\\Dropbox\\Coding\\Python\\Sports\\Soccer\\Data\\Clean Data\\'
main(path=sb_path, date=date_of_file)
