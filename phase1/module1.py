import sys
from collections import deque
sys.path.append(r'..\project-template')
from phase0.FA_class import DFA, State
from visualization import visualizer
from utils import utils
from math import log2
from utils.utils import imageType


def solve(image: imageType) -> 'DFA':
    image_str_states: dict[str, State] = {}
    dfa = DFA()
    dfa.alphabet = {'0','1','2','3'}
    s = add_state(dfa, image, image_str_states)
    dfa.init_state = s

    queue = deque(dfa.states)
    while len(queue) != 0 :
        state = queue.pop()
        # path = state.path_to_state
        image = state.image
        if len(image) > 1:
            for q in dfa.alphabet:
                # print( state.image)
                # print('q', q)
                new_image = zoom_image(image,q)
                # print('new image', new_image,'\n')
                new_image_str = convert_image(new_image)
                if new_image_str in image_str_states.keys():
                    state.add_transition(q, image_str_states[new_image_str])
                else:
                    new_state = add_state(dfa, new_image, image_str_states)
                    queue.appendleft(new_state)
                    state.add_transition(q, new_state)
        else:
            for q in dfa.alphabet:
                state.add_transition(q, state)
            if image[0][0]:
                dfa.final_states.add(state)
    return dfa

def add_state(dfa: DFA, image: imageType, image_str_states: dict[str, State]):
    s = State(None)
    s.add_image(image)
    image_str_states[convert_image(image)] = s
    dfa.state_ids[s.id] = s
    dfa.states.append(s)
    return s

def convert_image(image: imageType)-> str:
    l = []
    for i in image:
        l += [str(j) for j in i] 
    return ''.join(l) 

def zoom_image(image: imageType, addr)-> list[list[int]]: 
    size = len(image)
    if size > 0:
        max_addr_len = log2(size)
    else:
        max_addr_len = 1
    row,col = address_to_row_col(addr,size)
    if len(addr) == max_addr_len:
        return [[image[row][col]]]
    else:
        l = []
        offset = int(2**(max_addr_len-len(addr)))
        for r in range(row, row+offset):
            l.append(image[r][col:col+offset])
        return l
    
def address_to_row_col(address,size):
    if address:
        div = {'0':[0,0],'1':[0,1],'2':[1,0],'3':[1,1]} #sec number: [row,col]
        row, col = 0,0
        scale = size/2
        ind = 0
        while ind < len(address)-1:
            row += scale*div[address[ind]][0]
            col += scale*div[address[ind]][1]
            scale/= 2
            ind += 1
        row += scale*div[address[ind]][0]
        col += scale*div[address[ind]][1]
        return int(row), int(col)
    else:
        return 0,0
        

def row_col_to_address(row,col,size):
    # cols_div = {0:['0','3'], 1:['1','2']}
    rows_div = {0: ['2','3'], 1:['0','1']} #sec remainder of row and col
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
    image = [[1, 1, 1, 1],
             [1, 0, 1, 0],
             [0, 1, 0, 1],
             [1, 1, 1, 1]]

    utils.save_image(image)
    # print(convert_image(zoom_image(image,'0')))
    fa = solve(image)
    print(fa.serialize_json())
