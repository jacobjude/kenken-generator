class Box:
    def __init__(self, value, pos_in_array, is_in_cage=False):
        self.value = value
        # the second parameter gives the position of the box in the board as if it was a 1D array

        self.pos_in_array = pos_in_array
        self.is_in_cage = is_in_cage

    def __eq__(self, other):
        return self.pos_in_array == other.pos_in_array

    def __str__(self):
        return f"[val: {self.value} pos: {self.pos_in_array}]"
