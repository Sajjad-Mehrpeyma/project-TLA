import sys
sys.path.append(r'..\project-template')
from phase0.FA_class import DFA
from utils import utils
from utils.utils import imageType


def solve(json_str: str, image: imageType) -> bool:
    total = len(image)**2
    miss = 0
    fa = DFA.deserialize_json(json_str)
    for row in range(len(image)):
        for col in range(len(image)):
            addr = row_col_to_address(row, col, len(image))
            state = fa.init_state
            for char in addr:
                state = state.transitions[char]
            if fa.is_final(state) != image[row][col]:
                miss += 1

    return True if not miss else False,1-miss/total

def row_col_to_address(row, col, size):
    # cols_div = {0:['0','3'], 1:['1','2']}
    rows_div = {0: ['0','1'], 1:['2','3']} #sec remainder of row and col
    scale = size/2
    addr = ''
    while scale != 1:
        addr += rows_div[int(row//scale)][int(col//scale)]
        row %= scale
        col %= scale
        scale/=2
    addr += rows_div[int(row//scale)][int(col//scale)]
    return addr

if __name__ == "__main__":
    print(
        solve(
            '{"states": ["q_0", "q_1", "q_2", "q_3", "q_4"], "initial_state": "q_0", "final_states": ["q_3"], '
            '"alphabet": ["0", "1", "2", "3"], "q_0": {"0": "q_1", "1": "q_1", "2": "q_2", "3": "q_2"}, "q_1": {"0": '
            '"q_3", "1": "q_3", "2": "q_3", "3": "q_4"}, "q_2": {"0": "q_4", "1": "q_3", "2": "q_3", "3": "q_3"}, '
            '"q_3": {"0": "q_3", "1": "q_3", "2": "q_3", "3": "q_3"}, "q_4": {"0": "q_4", "1": "q_4", "2": "q_4", '
            '"3": "q_4"}}',
            [[1, 1, 1, 1],
             [1, 0, 1, 0],
             [0, 1, 0, 1],
             [1, 1, 1, 1]]
        )
    )
