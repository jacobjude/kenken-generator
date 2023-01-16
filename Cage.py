class Cage:
    def __init__(self, boxes, operator="", target_num=0):
        self.target_num = target_num
        self.boxes = boxes
        self.operator = operator
        self.cage_size = len(boxes)

    def __str__(self):
        ret = ""
        for i in self.boxes:
            ret = ret + str(i) + " -- "
        return self.operator + ": " + ret

    def __eq__(self, other):
        return other.boxes[0] == self.boxes[0]

    def assign_target(self):

        match self.operator:
            case "+":
                sum = 0
                for i in self.boxes:
                    sum += i.value
                self.target_num = sum
            case "-":
                vals = [x.value for x in self.boxes]
                self.target_num = max(vals) - min(vals)
            case "x":
                self.target_num = 1
                for i in self.boxes:
                    self.target_num *= i.value
            case "÷":
                vals = [x.value for x in self.boxes]
                self.target_num = int(max(vals) / min(vals))

    def is_in_cage(self, box):
        return box in self.boxes

