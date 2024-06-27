import sys
sys.path.append(r'..\..\project-template')
from phase0.FA_class import DFA, State
from visualization import visualizer
from utils import utils
from math import log2
from utils.utils import imageType


def solve(image: imageType) -> 'DFA':
    
    ...
def zoom_and_convert_image(image: imageType, addr, size):
    max_addr_len = log2(size)
    row,col = address_to_row_col(addr,size)
    if len(addr) == max_addr_len:
        return str(image[row][col])
    else:
        l = []
        offset = int(2**(max_addr_len-len(addr)))
        for r in range(row, row+offset):
            l += image[r][col:col+offset]
        l = [str(p) for p in l ]
        return ''.join(l)
    
def address_to_row_col(address,size):
    if address:
        div = {'0':[1,0],'1':[1,1],'2':[0,0],'3':[0,1]} #sec number: [row,col]
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
    # add = row_col_to_address(1,3,8)
    # add = '3'
    # print(address_to_row_col(add,4))
    image = [[1, 1, 1, 1],
             [1, 0, 1, 0],
             [0, 1, 0, 1],
             [1, 1, 1, 1]]

    utils.save_image(image)
    print(address_to_row_col('11',4))
    print(zoom_and_convert_image(image,'2',4))
    # fa = solve(image)
    # print(fa.serialize_json())
