
class StringUtils:

    def __init__(self, str):
        self.str = str

    def getRoot(self):
        root = ""
        root += self.str[0]
        if self.str[1] == 'b' or self.str[1] == '#':
            root += self.str[1]
        return root

    def getType(self):
        type = ['minor', 'major', 'm7', 'm9']