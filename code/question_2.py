from process_game_state import ProcessGameState
import pandas as pd
import matplotlib.pyplot as plt
import warnings
warnings.filterwarnings("ignore")

def question_2a(game_state_df):
    team2_T_alive = game_state_df[(game_state_df['side'] == 'T') & (game_state_df['team'] == 'Team2') & (game_state_df['is_alive'] == True)]

    team2_T_alive_distinct = team2_T_alive[['round_num', 'tick', 'player', 'in_choke_area']].drop_duplicates()
    team2_T_alive_distinct['Rank'] = team2_T_alive_distinct.groupby(by=['round_num', 'player'])['tick'].transform(lambda x: x.rank())

    team2_T_alive_distinct_earliest_tick = team2_T_alive_distinct[(team2_T_alive_distinct['Rank'] == 1)]

    players_entering_choke_area = team2_T_alive_distinct_earliest_tick['in_choke_area'].value_counts().to_dict()
    players_entering_choke_area[True] = 0 if not players_entering_choke_area.__contains__(True) else players_entering_choke_area[True]
    players_entering_choke_area[False] = 0 if not players_entering_choke_area.__contains__(False) else players_entering_choke_area[False]
    
    return "Yes" if players_entering_choke_area[True] >= players_entering_choke_area[False] else "No"



def question_2b(game_state_df):

    def clock_time_seconds(clock_time):
        min_str, sec_str = clock_time.split(':')
        return int(min_str)*60 + int(sec_str)


    team2_T_alive = game_state_df[(game_state_df['side'] == 'T') & (game_state_df['team'] == 'Team2') & (game_state_df['is_alive'] == True) & (game_state_df['area_name'] == 'BombsiteB')]

    team2_T_alive_distinct = team2_T_alive[['round_num', 'tick', 'player', 'weapon_class', 'clock_time', 'seconds']].drop_duplicates()
    team2_T_alive_distinct['Rank'] = team2_T_alive_distinct.groupby(by=['round_num', 'player', 'weapon_class'])['tick'].rank(method='first', ascending=True)

    team2_T_alive_distinct_earliest_tick = team2_T_alive_distinct[(team2_T_alive_distinct['Rank'] == 1)]
    t2_2_rifles_or_smgs = team2_T_alive_distinct_earliest_tick[(team2_T_alive_distinct_earliest_tick['weapon_class'] == 'Rifle') | (team2_T_alive_distinct_earliest_tick['weapon_class'] == 'SMG')]
    t2_2_rifles_or_smgs['clock_time_secs'] = t2_2_rifles_or_smgs.apply(lambda x: clock_time_seconds(x['clock_time']), axis=1)

    groupby_cnt = t2_2_rifles_or_smgs.groupby(['round_num', 'weapon_class']).size().reset_index(name='weapon_count')
    groupby_cnt_2_or_more = groupby_cnt[groupby_cnt['weapon_count'] >= 2]
    df_merged = pd.merge(t2_2_rifles_or_smgs, groupby_cnt_2_or_more, on = 'round_num', how = 'inner')
    avg_time = df_merged['clock_time_secs'].mean() 
    return f"0{int(avg_time//60)}:{int(round(avg_time%60))}" if int(avg_time//60) < 10 else f"{int(avg_time//60)}:{int(round(avg_time%60))}"



def question_2c(game_state_df):
    team1_CT_alive = game_state_df[(game_state_df['side'] == 'CT') & (game_state_df['team'] == 'Team2') & (game_state_df['is_alive'] == True) & (game_state_df['area_name'] == 'BombsiteB')]
    team1_CT_alive_1 = team1_CT_alive[['x', 'y', 'player']].drop_duplicates()
    plt.hist2d(team1_CT_alive_1['x'], team1_CT_alive_1['y'])
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig('output/result.png')
    return "Check the heatmap image saved the output directory! (output/result.png)"