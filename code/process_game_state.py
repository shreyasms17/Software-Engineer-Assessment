import pandas as pd


class ProcessGameState:
    def __init__(self, input_file_path):
        self.bounding_polygon = [(-1735, 250), (-2024, 398), (-2806, 742), (-2472, 1233), (-1565, 580)]
        self.game_state_df = None
        self.input_file_path = input_file_path
    
    def read_input(self) -> None:
        self.game_state_df = pd.read_parquet(self.input_file_path)

    def check_in_choke_area(self, x, y, z) -> None:
        if z < 285 or z > 421:
            return False
        else:
            is_inside = False
            npol = 5
            for i in range(npol):
                j = (i - 1 + npol) % npol
                if (((self.bounding_polygon[i][1] <= y and y < self.bounding_polygon[j][1]) or (self.bounding_polygon[j][1] <= y and y < self.bounding_polygon[i][1])) and
                        (x < (self.bounding_polygon[j][0] - self.bounding_polygon[i][0]) * (y - self.bounding_polygon[i][1]) / (self.bounding_polygon[j][1] - self.bounding_polygon[i][1]) + self.bounding_polygon[i][0])):
                    is_inside = not is_inside
            return is_inside

    def compute_row_position(self) -> None:
        self.game_state_df['in_choke_area'] = self.game_state_df.apply(lambda row: self.check_in_choke_area(row['x'], row['y'], row['z']), axis = 1)

    def get_weapon_classes(self) -> None:
        self.game_state_df = self.game_state_df.explode('inventory')
        self.game_state_df['weapon_class'] = self.game_state_df['inventory'].apply(lambda x: x['weapon_class'] if x else None)
    
    def get_processed_game_state(self) -> pd.core.frame.DataFrame:
        self.read_input()
        self.compute_row_position()
        self.get_weapon_classes()
        return self.game_state_df