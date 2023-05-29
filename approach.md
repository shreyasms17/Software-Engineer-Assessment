## Approach


#### Question 1
A class ProcessGameState was created with class variables

    1. bounding_polygon which describes outer points the light blue area denoting the choke area
    2. game_state_df, a dataframe placeholder to hold the dataframe
    3. input parquet file path

The class methods include:

    1. read_input, that reads the input parquet file into the game_state_df dataframe
    2. check_in_choke_area, that checks if a particular coordinate falls inside the choke area
    3. compute_row_position, which checks if a row in the dataframe is inside the choke area or not and creates a boolean column in game_state_df called 'in_choke_area'
    4. get_weapon_classes, that adds a weapon_class column by exploding the inventory column and creating a row for each weapon carried by a player at a given point of time
    5. get_processed_game_state, returns the processed game state dataframe



#### Question 2a
To check if entering via the choke area is the common strategy used by terrorist side of Team2, we check if the members is alive first.
Since every round counts as an entry for a player, we check at the round, tick, and player grain level.
The earliest tick is retrieved by implementing the rank logic only to see whether the player's initial area in a round was in the choke area or not.
The counts were then compared, and entering through the common area was not a common strategy at all.


#### Question 2b
To get the average clock time when Team2 on terrorist side enters “BombsiteB” with least 2 rifles or SMG, we first filter on the team membership, terrorist side and them being alive.
The rows with earliest tick is then obtained via the rank logic that shows their first entry into BombsiteB.
A filter is applied on Rifles and SMGs and the weapon count is obtained by doing a group by on the round number and the weapon class and then the condition for each weapon is checked.
Only those rounds with Rifle count >= 2 or SMG count >= 1 are filtered and the avg clock time is calculated for all members in that round.


#### Question 2c 
A heatmap was constructed based on the positions of Team2 on the CT side inside BombsiteB along with two reference points (point 17 and 13) of the choke area to get a relative position of where the members would be waiting inside the BombsiteB.


#### Question 3
Approach is provided in Q3_design.md