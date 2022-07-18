class JackTokenizer:
    def __init__(self, filename):
        self.file = []
        file = open(filename, 'r')
        self.current_token = ''
        self.line_number = 0
        self.current_index = 0  # the current index of the line our token is on

        for line in file:
            line = line.strip(' ')
            self.file.append(line[:-1])

    def hasMoreTokens(self):
        return not ((self.line_number >= len(self.file) - 1) and (self.current_index + len(self.current_token) >= (len(self.file[self.line_number]))))

    def advance(self):
        # for now, just advance for every word
        # but first, we have to find the starting line index of our token which will be our self.currentIndex.
        token_start = self.current_index + len(self.current_token)
        if token_start >= len(self.file[self.line_number]) - 1:
            self.line_number += 1
            self.current_index = 0
        else:
            self.current_index = token_start

        restOfLine = self.file[self.line_number][token_start:]

        self.current_token = restOfLine[:restOfLine.index(' ')]

        print(restOfLine + "|")
        print(self.current_token + "|")
