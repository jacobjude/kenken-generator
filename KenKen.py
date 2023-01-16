from generation import *

class KenKen:

    def __init__(self, size, av_ops, max_cage_size):
        self.size = size
        self.av_ops = av_ops
        self.max_cage_size = max_cage_size
        self.board = self.generate_board()
        self.boxes = self.generate_boxes()
        self.cages = self.create_cages()


    def __str__(self):
        ret = ""
        for i in self.board:
            ret += str(i) + "\n"

        for i in self.cages:
            ret += str(i) + "\n"
        return ret

    def get_cagesize_probability(self):
        if self.av_ops == ["", "-", "", "÷"]:
            return 1.0
        return (self.av_ops.count("÷") + self.av_ops.count("-")) / (2 + self.av_ops.count("+") + self.av_ops.count("x"))

    def generate_board(self):
        # generate a size x size board in the form of a 2D array
        # initialize a size x size array with zeros
        arr = [[0 for i in range(self.size)] for i in range(self.size)]

        # the possible values that a row or column might have (1 - size)
        possible_values = [x for x in range(1, self.size + 1)]

        # fill the array with values from 1 - size such that each column and row does not
        # repeat any numbers
        for i in range(self.size):
            for j in range(self.size):
                arr[i][j] = possible_values[j - i]

        # randomize the board 100000 times
        for i in range(100000):
            # first, switch two random rows.
            # this method ensures that row1 and row2 are different
            row1 = random.randint(0, self.size - 1)
            row2 = random.randint(0, self.size - 2)
            if row2 >= row1:
                row2 += 1

            # next, switch two random columns (using the same method as above)
            switch_rows(arr, row1, row2)
            col1 = random.randint(0, self.size - 1)
            col2 = random.randint(0, self.size - 2)
            if col2 >= col1:
                col2 += 1
            switch_columns(arr, col1, col2)

        # 50/50 chance to transpose the array
        if random.randint(0, 1):
            arr = [[row[i] for row in arr] for i in range(len(arr[0]))]

        return arr

    def generate_boxes(self):
        # create a list of boxes for each value in the array
        boxes = []
        for i in range(len(self.board)):
            for j in range(len(self.board)):
                boxes.append(Box(self.board[i][j], i * len(self.board) + j))
        return boxes

    def get_available_directions(self, rand_cage_size, cage_index, boxes):
        # finds an available path for the cage generator to travel in
        # checks if adjacent boxes are neighbors and not already in a cage.
        available_directions = [1, 2, 3, 4]  # 1 = up, 2 = right, 3 = down, 4 = left
        try:
            if boxes[cage_index - self.size].is_in_cage is True or \
                    not are_neighbors(boxes[cage_index], boxes[cage_index - self.size], self.size):
                available_directions.remove(1)
        except:
            available_directions.remove(1)

        try:
            if boxes[cage_index + 1].is_in_cage is True or \
                    not are_neighbors(boxes[cage_index], boxes[cage_index + 1], self.size):
                available_directions.remove(2)
        except:
            available_directions.remove(2)

        try:
            if boxes[cage_index + self.size].is_in_cage is True or \
                    not are_neighbors(boxes[cage_index], boxes[cage_index + self.size], self.size):
                available_directions.remove(3)
        except:
            available_directions.remove(3)

        try:
            if boxes[cage_index - 1].is_in_cage is True or \
                    not are_neighbors(boxes[cage_index], boxes[cage_index - 1], self.size):
                available_directions.remove(4)
        except:
            available_directions.remove(4)

        return available_directions

    def create_cages(self):
        # create cages until the whole board is caged

        cages = []
        whole_board_caged = False
        cage_size_prob = self.get_cagesize_probability()  # probability that a cage will be size 2
        # print("cage size 2 prob: " + str(cage_size_prob))
        if cage_size_prob == 0:
            div_sub_out_of_2sized_cages = 0
        elif cage_size_prob == 1.0:
            div_sub_out_of_2sized_cages = 1.0
        else:
            div_sub_out_of_2sized_cages = 0.5 / cage_size_prob  # prob that an operator in a cage of size 2 will be div/sub
        # print("out of size 2 cages, prob of div sub: " + str(div_sub_out_of_2sized_cages))

        while not whole_board_caged:
            # find the first uncaged box and save its index. break the loop if the whole board has been caged
            whole_board_caged = True
            for i in range(len(self.boxes)):
                if not self.boxes[i].is_in_cage:
                    whole_board_caged = False
                    index = i
                    break
            if whole_board_caged:
                break

            # start a cage with a random size. save the boxes in that cage in a list
            if random.random() < cage_size_prob:
                rand_cage_size = 1
            else:
                rand_cage_size = random.randint(2, self.max_cage_size)

            cage_boxes = []
            cage_index = index

            # save the current box since we know it's uncaged (from the for loop above)
            cage_boxes.append(self.boxes[cage_index])
            self.boxes[cage_index].is_in_cage = True

            for i in range(rand_cage_size):
                # find an available direction to travel in
                available_directions = self.get_available_directions(rand_cage_size, cage_index, self.boxes)

                # if available_directions is empty, the except clause will run. this creates a cage of size 1 and exits
                try:
                    direction = random.choice(available_directions)
                except:
                    if self.boxes[cage_index] not in cage_boxes:
                        cage_boxes.append(self.boxes[cage_index])
                        cages.append(cage_boxes)
                    self.boxes[cage_index].is_in_cage = True
                    cage_index += 1
                    break

                match direction:
                    case 1:  # up
                        cage_index = cage_index - self.size
                        self.boxes[cage_index].is_in_cage = True
                        cage_boxes.append(self.boxes[cage_index])

                    case 2:  # right
                        cage_index = cage_index + 1
                        self.boxes[cage_index].is_in_cage = True
                        cage_boxes.append(self.boxes[cage_index])
                    case 3:  # down
                        cage_index = cage_index + self.size
                        self.boxes[cage_index].is_in_cage = True
                        cage_boxes.append(self.boxes[cage_index])
                    case 4:  # left
                        cage_index = cage_index - 1
                        self.boxes[cage_index].is_in_cage = True
                        cage_boxes.append(self.boxes[cage_index])

            cages.append(Cage(cage_boxes))

            # get operator for new cage
            while cages[-1].operator == "":
                assign_operator(self.av_ops, cages, div_sub_out_of_2sized_cages)

            # assign target for new cage
            cages[-1].assign_target()

        return cages


def assign_operator(av_ops, cages, div_sub_out_of_2sized_cages):
    chance = random.random()
    if cages[-1].cage_size == 2:
        if chance < div_sub_out_of_2sized_cages:
            if cages[-1].boxes[0].value % cages[-1].boxes[1].value == 0 \
                    or cages[-1].boxes[1].value % cages[-1].boxes[0].value == 0:
                cages[-1].operator = av_ops[random.randint(2, 3)]
            elif "-" in av_ops:
                cages[-1].operator = "-"
            else:
                new_cage1 = [cages[-1].boxes[0]]
                new_cage2 = [cages[-1].boxes[1]]
                cages.pop(-1)
                cages.append(Cage(new_cage1))
                cages.append(Cage(new_cage2))
        else:
            if av_ops.count("+") == 1 and av_ops.count("x") == 1:
                cages[-1].operator = av_ops[random.randint(0, 1)]
            elif av_ops.count("+") == 1:
                cages[-1].operator = "+"
            else:
                cages[-1].operator = "x"
    else:
        if av_ops.count("+") == 1 and av_ops.count("x") == 1:
            cages[-1].operator = av_ops[random.randint(0, 1)]
        elif av_ops.count("+") == 1:
            cages[-1].operator = "+"
        else:
            cages[-1].operator = "x"


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







