import random
from Cage import Cage
from Box import Box


def print_2D_array(arr):
    for i in arr:
        print(i)



def switch_columns(arr, col1, col2):
    # switch col1 and col2 in arr
    temp_column = []
    for i in range(len(arr)):
        temp_column.append(arr[i][col1])
        arr[i][col1] = arr[i][col2]
        arr[i][col2] = temp_column[i]


def switch_rows(arr, row1, row2):
    # switch row1 and row2 in arr
    temp = arr[row1]
    arr[row1] = arr[row2]
    arr[row2] = temp


def are_neighbors(box1, box2, size):
    # checks if box1 and box2 are adjacent to each other on the board (but not on a diagonal)
    
    # if box2 is below or above box1, it is adjacent
    if (box1.pos_in_array == box2.pos_in_array - size or
            box1.pos_in_array == box2.pos_in_array + size):
        return True

    # if box2 is to the right or left of box 1, it is adjacent. if box1 is on the edge of the board, 
    # only check in the inward direction
    if ((box1.pos_in_array % size != 0 and box1.pos_in_array % size != (size - 1)) and
            (box1.pos_in_array == box2.pos_in_array - 1 or box1.pos_in_array == box2.pos_in_array + 1)):
        return True
    elif box1.pos_in_array % size != 0 and box1.pos_in_array == box2.pos_in_array + 1:
        return True
    elif box1.pos_in_array % size != (size - 1) and box1.pos_in_array == box2.pos_in_array - 1:
        return True
    
    # if box1 and box2 aren't adjacent, return false
    return False

