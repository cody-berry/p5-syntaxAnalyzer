class JackTokenizer:
    def __init__(self, filename):
        self.file = []
        file = open(filename, 'r')
        self.currentToken = ''
        self.lineNumber = 0
        self.currentIndex = 0  # the current index of the line our token is on

        for line in file:
            line = line.strip(' ')
            self.file.append(line[:-1])

    def hasMoreTokens(self):
        return not ((self.lineNumber >= len(self.file) - 1) and (self.currentIndex + len(self.currentToken) >= (len(self.file[self.lineNumber]))))