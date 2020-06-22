import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import Arc, Rectangle


def draw_pitch(ax):
    '''
    Source: https://fcpython.com/visualisation/drawing-pitchmap-adding-lines-circles-matplotlib
    '''
    # size of the pitch is 120, 80
    # Create figure

    # Pitch Outline & Centre Line
    plt.plot([0, 0], [0, 80], color="black")
    plt.plot([0, 120], [80, 80], color="black")
    plt.plot([120, 120], [80, 0], color="black")
    plt.plot([120, 0], [0, 0], color="black")
    plt.plot([60, 60], [0, 80], color="black")

    # Left Penalty Area
    plt.plot([14.6, 14.6], [57.8, 22.2], color="black")
    plt.plot([0, 14.6], [57.8, 57.8], color="black")
    plt.plot([0, 14.6], [22.2, 22.2], color="black")

    # Right Penalty Area
    plt.plot([120, 105.4], [57.8, 57.8], color="black")
    plt.plot([105.4, 105.4], [57.8, 22.5], color="black")
    plt.plot([120, 105.4], [22.5, 22.5], color="black")

    # Left 6-yard Box
    plt.plot([0, 4.9], [48, 48], color="black")
    plt.plot([4.9, 4.9], [48, 32], color="black")
    plt.plot([0, 4.9], [32, 32], color="black")

    # Right 6-yard Box
    plt.plot([120, 115.1], [48, 48], color="black")
    plt.plot([115.1, 115.1], [48, 32], color="black")
    plt.plot([120, 115.1], [32, 32], color="black")

    # Prepare Circles
    centreCircle = plt.Circle((60, 40), 8.1, color="black", fill=False)
    centreSpot = plt.Circle((60, 40), 0.71, color="black")
    leftPenSpot = plt.Circle((9.7, 40), 0.71, color="black")
    rightPenSpot = plt.Circle((110.3, 40), 0.71, color="black")

    # Draw Circles
    ax.add_patch(centreCircle)
    ax.add_patch(centreSpot)
    ax.add_patch(leftPenSpot)
    ax.add_patch(rightPenSpot)

    # Prepare Arcs
    # arguments for arc
    # x, y coordinate of centerpoint of arc
    # width, height as arc might not be circle, but oval
    # angle: degree of rotation of the shape, anti-clockwise
    # theta1, theta2, start and end location of arc in degree
    leftArc = Arc((9.7, 40), height=16.2, width=16.2, angle=0, theta1=310, theta2=50, color="black")
    rightArc = Arc((110.3, 40), height=16.2, width=16.2, angle=0, theta1=130, theta2=230, color="black")

    # Draw Arcs
    ax.add_patch(leftArc)
    ax.add_patch(rightArc)


def draw_half_pitch(ax):
    '''Draws half a soccer field - Better for shot charts than full pitch'''
    # focus on only half of the pitch
    # Pitch Outline & Centre Line
    Pitch = Rectangle([60, 0], width=60, height=80, fill=False)
    # Right Penalty Area
    RightPenalty = Rectangle([105.4, 22.3], width=14.6, height=35.3, fill=False)

    # Right 6-yard Box
    RightSixYard = Rectangle([115.1, 32], width=4.9, height=16, fill=False)

    # Prepare Circles
    centreCircle = Arc((60, 40), width=8.1, height=8.1, angle=0, theta1=270, theta2=90, color="black")
    centreSpot = plt.Circle((60, 40), 0.71, color="black")
    rightPenSpot = plt.Circle((110.3, 40), 0.71, color="black")
    rightArc = Arc((110.3, 40), height=16.2, width=16.2, angle=0, theta1=130, theta2=230, color="black")

    element = [Pitch, RightPenalty, RightSixYard, centreCircle, centreSpot, rightPenSpot, rightArc]
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


def main(comp=49, season=3, player_list=None, team_number=766, team_summary=False):
    #### Housekeeping Lists ####
    defensive_actions = ['Interception', 'Clearance', 'Duel', 'Block', 'Pressure']
    tackle_outcomes_good = ['Success In Play', 'Won']
    tackle_outcomes_bad = ['Lost Out', 'Lost In Play']  # 'None' always goes with aerial loss afaik

    duels_lost = pd.DataFrame()
    df = pd.read_csv('SB_events_{0}_{1}.csv'.format(comp, season))
    # df = pd.read_csv('SB_events_%d_%d.csv' % (comp, season))
    print(df.head(25).to_string())
    print(df['start_location_x'].head(10).to_string())

    #### Subset Defensive Actions
    defensive_actions = df[(df['type_name'].isin(defensive_actions))]
    # print((defensive_actions).head(10).to_string())
    # print(len(defensive_actions))

    interceptions = defensive_actions[defensive_actions['type_name'] == 'Interception']
    clearances = defensive_actions[defensive_actions['type_name'] == 'Clearance']
    duels = defensive_actions[defensive_actions['type_name'] == 'Duel']
    blocks = defensive_actions[defensive_actions['type_name'] == 'Block']
    pressures = defensive_actions[defensive_actions['type_name'] == 'Pressure']

    # duels_won = duels[duels['outcome'].isin(tackle_outcomes_good)]
    # duels_lost = duels[duels['outcome'].isin(tackle_outcomes_bad)

    for player in player_list:
        print(player)
        ### Draw the Pitch ###
        ###     Full Pitch for defensive actions ###
        fig = plt.figure()
        fig.set_size_inches(7, 5)
        ax = fig.add_subplot(1, 1, 1)
        draw_pitch(ax)
        plt.ylim(-1, 80)
        plt.xlim(-1, 121)
        # plt.legend(loc='upper right')
        plt.axis('off')

        interceptions_player = interceptions[interceptions['player_name'] == player]
        clearances_player = clearances[clearances['player_name'] == player]
        duels_won_player = duels[(duels['player_name'] == player) & (duels['duel_outcome_name'].isin(tackle_outcomes_good))]
        duels_lost_player = duels[(duels['player_name'] == player) & (duels['duel_outcome_name'].isin(tackle_outcomes_bad))]
        pressures_player = pressures[pressures['player_name'] == player]

        ax.scatter(interceptions_player['start_location_x'], interceptions_player['start_location_y'], c='green',
                   label='Interceptions', s=11, marker='o')
        ax.scatter(duels_won_player['start_location_x'], duels_won_player['start_location_y'], c='blue',
                   label='Duels Won', s=11, marker='v')
        ax.scatter(duels_lost_player['start_location_x'], duels_lost_player['start_location_y'], c='red',
                   label='Duels Lost', s=11, marker='x')
        ax.scatter(clearances_player['start_location_x'], clearances_player['start_location_y'], c='black', label='Clearances', s=11, marker='s')
        ax.scatter(pressures_player['start_location_x'], pressures_player['start_location_y'], c='magenta', label='Pressures', s=11, marker='8')

        player_name_for_filesave = player.replace('"', "")  # The apostrophe was killing me...
        player = player.replace('"', "'")

        plt.legend(loc='upper right')
        plt.title('Defensive Actions for %s' % player)
        # plt.savefig('Defensive Actions %s.png' % player_name_for_filesave)
        plt.show()
        plt.close()

playerlist = ['Cari Roccaro', 'Abby Erceg']

main(comp=49, season=3, player_list=playerlist, team_number=766, team_summary=False)
