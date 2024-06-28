import sys
sys.path.append(r'..\project-template')
from math import log2
from phase0.FA_class import DFA, State
from phase2.module2 import row_col_to_address
from utils import utils
from utils.utils import imageType


def solve(json_str: str, resolution: int) -> imageType:
    fa = DFA.deserialize_json(json_str)
    image = [ [0 for _ in range(resolution)] for _ in range(resolution)]
    for row in range(resolution):
        for col in range(resolution):
            addr = row_col_to_address(row, col, resolution)
            state = fa.init_state
            for q in addr:
                state = state.transitions[q]
            if fa.is_final(state):
                image[row][col] = 1    
    return image


if __name__ == "__main__":
    pic_arr = solve(
        '{"states": ["q_0", "q_1", "q_2", "q_3", "q_4"], "initial_state": "q_0", "final_states": ["q_3"], '
        '"alphabet": ["0", "1", "2", "3"], "q_0": {"0": "q_1", "1": "q_1", "2": "q_2", "3": "q_2"}, "q_1": {"0": '
        '"q_3", "1": "q_3", "2": "q_3", "3": "q_4"}, "q_2": {"0": "q_4", "1": "q_3", "2": "q_3", "3": "q_3"}, '
        '"q_3": {"0": "q_3", "1": "q_3", "2": "q_3", "3": "q_3"}, "q_4": {"0": "q_4", "1": "q_4", "2": "q_4", '
        '"3": "q_4"}}',
        4
    )
    print(pic_arr)
    # utils.save_image(pic_arr)
    
