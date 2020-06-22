import pandas as pd
import statsbomb as sb
import requests
from tqdm import tqdm
import numpy as np

'''
Heavily cribbed from Devin P
https://github.com/devinpleuler/analytics-handbook
https://colab.research.google.com/github/devinpleuler/analytics-handbook/blob/master/notebooks/data_extraction_and_transformation.ipynb
'''
#### Basic Statsbomb Data ####
base_url = "https://raw.githubusercontent.com/statsbomb/open-data/master/data/"
comp_url = base_url + "matches/{}/{}.json"
match_events_url = base_url + "events/{}.json"
match_lineups_url = base_url + "lineups/{}.json"

def get_sb_matches(matches, team_list=None):

    match_list = []
    matches_for_team = pd.DataFrame()  # Empty DF for matches


    if team_list is not None:
        home_condition = (matches['home_team'].isin(team_list))  # Condition for Home Matches
        away_condition = (matches['away_team'].isin(team_list))  # Condition for Away Matches

        matches_for_team = matches_for_team.append(matches[home_condition]).append(matches[away_condition])
        matches = matches_for_team

    match_list = [m for m in matches['match_id']]

    return match_list


def get_sb_events(match_list):
    all_events = pd.DataFrame()

    print('Events')
    for m in tqdm(match_list):
        df_temp = pd.json_normalize(requests.get(url=match_events_url.format(m)).json())
        df_temp['match_id'] = m
        all_events = all_events.append(df_temp)

    location_columns = [x for x in all_events.columns.values if 'location' in x]

    for col in location_columns:
        for i, dimension in enumerate(['location_x', 'location_y']):
            new_col = col.replace('location', dimension)
            all_events[new_col] = all_events.apply(lambda x: x[col][i] if type(x[col]) == list else None, axis=1)
    print(all_events.head(1).to_string())

    ### Clean Up Variable Names
    all_events.columns = all_events.columns.str.replace(".", "_")

    return all_events


def get_sb_lineups(match_list):
    all_lineups = pd.DataFrame()

    print('Lineups')
    for m in tqdm(match_list):
        # print(m)
        # print(match_lineups_url.format(m))
        df_temp = pd.json_normalize(requests.get(url=match_lineups_url.format(m)).json())
        df_temp['match_id'] = m
        all_lineups = all_lineups.append(df_temp)

    return all_lineups


def sb_data_extract(path='', competition=49, season=3, events=True,
                    lineups=False, team_list=None, date='', return_data=False):

    matches = sb.Matches(competition, season).get_dataframe()  # Call SB Parser

    match_list = get_sb_matches(matches, team_list)

    if events:
        events_df = pd.DataFrame()
        events_df = get_sb_events(match_list)
        events_df.to_csv('{0}{1}SB_events_{2}_{3}.csv'.format(path, date, competition, season))
        print('Saved Event data on {0}{1}SB_data_{2}_{3}'.format(path, date, competition, season))

    if lineups:
        lineups_df = pd.DataFrame()
        lineups_df = get_sb_lineups(match_list)
        lineups_df.to_csv('{0}{1}SB_lineups_{2}_{3}.csv'.format(path, date, competition, season))
        print('Saved Lineup data on {0}{1}SB_data_{2}_{3}'.format(path, date, competition, season))

def main(comp_list=None, date='', path='', events=True, lineups=False):
    for thing in comp_list:
        this_comp = thing[0]
        this_season = thing[1]

        print("Competition: {}\nSeason: {}".format(this_comp, this_season))

        sb_data_extract(path=path, competition=this_comp, season=this_season, events=events, lineups=lineups,
                        team_list=None, date=date, return_data=False)


location_columns_hard_coded = ['location', 'pass_end_location', 'carry_end_location', 'shot_end_location', 'goalkeeper_end_location']

comp = 49
season_number = 3
date_for_file = '200526'
date_for_file = '200609'

save_path = 'C:\\Users\\JaysC\\Dropbox\\Coding\\Python\\Sports\\Soccer\\Data\\Clean Data\\'
save_path = 'C:\\Users\\JaysC\\Dropbox\\Coding\\Python\\Sports\\Soccer\\Data\\clean_data\\'

list_of_comps = [(49, 3), (37, 42), (37, 4), (11, 4), (11, 1), (43, 3), (72, 30)]

main(comp_list= list_of_comps, date=date_for_file, path=save_path, events=False, lineups=True)
