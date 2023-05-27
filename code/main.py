from process_game_state import ProcessGameState
import warnings
from question_2 import *

warnings.filterwarnings("ignore")

obj = ProcessGameState('data/game_state_frame_data.parquet')
game_state_df = obj.get_processed_game_state()

print(f"Q. Is entering via the light blue boundary a common strategy used by Team2 on T (terrorist) side?\nAns. {question_2a(game_state_df)}\n")

print(f"Q. What is the average timer that Team2 on T(terrorist) side enters BombsiteB with least 2 rifles or SMGs?\nAns. {question_2b(game_state_df)}\n")

print(f"Q. Where do you suspect Team 2's CT to be waiting inside BombsiteB ?\nAns. {question_2c(game_state_df)}")    