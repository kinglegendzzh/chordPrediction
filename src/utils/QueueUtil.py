class Queue():
    def __init__(self, array = None):
        self.array = array

    def length(self):
        if not self.array:
            return 0
        else:
            return len(self.array)

    def is_Empty(self):
        return self.array == None

    def push(self, value):
        self.array.append(value)

    def pop(self):
        self.array.pop(0)

    def top(self):
        return self.array[0]

    def travel(self):
        print(self.array)

    def index(self, i):
        return self.array[i]

    def remove(self, index):
        return self.array.pop(index)

    def clear(self):
        self.array.clear()

    def last(self):
        if self.length()!=0:
            return self.array[self.length()-1]

