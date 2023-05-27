from process_game_state import ProcessGameState
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

def question_2a(game_state_df) -> str:
    """
    Analyzes the game state data to determine if entering the choke area is a common strategy used players from Team2 on T-side.
    
    Parameters:
    - game_state_df (pd.core.frame.DataFrame): The game state data DataFrame.
    
    Returns:
    - str: "Yes" if more players enter the choke area, "No" otherwise.
    """

    # gets all members of Team 2 on T side who are alive
    team2_T_alive = game_state_df[(game_state_df['side'] == 'T') & (game_state_df['team'] == 'Team2') & (game_state_df['is_alive'] == True)]

    # drop all duplicate rows
    team2_T_alive_distinct = team2_T_alive[['round_num', 'tick', 'player', 'in_choke_area']].drop_duplicates()

    # rank on tick and select earliest tick so we know where the player entered the round from
    team2_T_alive_distinct['Rank'] = team2_T_alive_distinct.groupby(by=['round_num', 'player'])['tick'].transform(lambda x: x.rank())
    team2_T_alive_distinct_earliest_tick = team2_T_alive_distinct[(team2_T_alive_distinct['Rank'] == 1)]

    # get value counts of if player entered from choke area or not
    players_entering_choke_area = team2_T_alive_distinct_earliest_tick['in_choke_area'].value_counts().to_dict()
    players_entering_choke_area[True] = 0 if not players_entering_choke_area.__contains__(True) else players_entering_choke_area[True]
    players_entering_choke_area[False] = 0 if not players_entering_choke_area.__contains__(False) else players_entering_choke_area[False]
    
    # if majority entered from choke area then return Yes else No
    return "Yes" if players_entering_choke_area[True] >= players_entering_choke_area[False] else "No"



def question_2b(game_state_df) -> str:
    """
    Analyzes the game state data to calculate the average clock time when Team2 on T(terrorist) side enters “BombsiteB” with least 2 rifles or SMG.
    
    Parameters:
    - game_state_df (pd.core.frame.DataFrame): The game state data DataFrame.
    
    Returns:
    - str: The average clock time in the format 'MM:SS'.
    """

    def clock_time_seconds(clock_time) -> int:
        min_str, sec_str = clock_time.split(':')
        return int(min_str)*60 + int(sec_str)

    # gets all members of Team 2 on T side who are alive and in BombsiteB
    team2_T_alive = game_state_df[(game_state_df['side'] == 'T') & (game_state_df['team'] == 'Team2') & (game_state_df['is_alive'] == True) & (game_state_df['area_name'] == 'BombsiteB')]

    # get earliest tick when they enter BombsiteB and filter on rank as 1
    team2_T_alive_distinct = team2_T_alive[['round_num', 'tick', 'player', 'weapon_class', 'clock_time', 'seconds']].drop_duplicates()
    team2_T_alive_distinct['Rank'] = team2_T_alive_distinct.groupby(by=['round_num', 'player', 'weapon_class'])['tick'].rank(method='first', ascending=True)
    team2_T_alive_distinct_earliest_tick = team2_T_alive_distinct[(team2_T_alive_distinct['Rank'] == 1)]

    # filter on only Rifles or SMGs
    t2_2_rifles_or_smgs = team2_T_alive_distinct_earliest_tick[(team2_T_alive_distinct_earliest_tick['weapon_class'] == 'Rifle') | (team2_T_alive_distinct_earliest_tick['weapon_class'] == 'SMG')]
    t2_2_rifles_or_smgs['clock_time_secs'] = t2_2_rifles_or_smgs.apply(lambda x: clock_time_seconds(x['clock_time']), axis=1)

    # get counts of rifles and SMG's in each round & filter only those with >= 2
    groupby_cnt = t2_2_rifles_or_smgs.groupby(['round_num', 'weapon_class']).size().reset_index(name='weapon_count')
    groupby_cnt_2_or_more = groupby_cnt[groupby_cnt['weapon_count'] >= 2]

    # merge the aggregated df on round number to get avg clock time
    df_merged = pd.merge(t2_2_rifles_or_smgs, groupby_cnt_2_or_more, on = 'round_num', how = 'inner')
    avg_time = df_merged['clock_time_secs'].mean() 
    return f"0{int(avg_time//60)}:{int(round(avg_time%60))}" if int(avg_time//60) < 10 else f"{int(avg_time//60)}:{int(round(avg_time%60))}"



def question_2c(game_state_df) -> str:
    """
    Generates a 2D histogram heatmap of the positions of Team2 on CT-side players inside 'BombsiteB' and saves it as an image.
    
    Parameters:
    - game_state_df (pd.core.frame.DataFrame): The game state data DataFrame.
    
    Returns:
    - str: A message indicating the location of the saved heatmap image.
    """
    team2_CT_alive = game_state_df[(game_state_df['side'] == 'CT') & (game_state_df['team'] == 'Team2') & (game_state_df['is_alive'] == True) & (game_state_df['area_name'] == 'BombsiteB')]
    team2_CT_alive = team2_CT_alive[['x', 'y', 'player']].drop_duplicates()
    plt.hist2d(team2_CT_alive['x'], team2_CT_alive['y'])
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig('output/result.png')
    return "Check the heatmap image saved the output directory! (output/result.png)"