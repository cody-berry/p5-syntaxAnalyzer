class JackTokenizer:
    def __init__(self, filename):
        self.file = []
        file = open(filename, 'r')
        self.current_token = ''
        self.line_number = 0
        self.current_index = 0  # the current index of the line our token is on

        for line in file:
            try:
                line = line[:(line.index('/'))]
            except:
                pass
            line = line.strip(' ')
            if len(line) > 0 and line[0] != '/':
                self.file.append(line[:-1])

    def hasMoreTokens(self):
        return not ((self.line_number >= len(self.file) - 1) and (
                self.current_index + len(self.current_token) >= (
                len(self.file[self.line_number]))))

    def advance(self):

        print(f'Token starting index: |{self.current_index}|')

        rest_of_line = self.file[self.line_number][self.current_index:]
        print(f'Rest of line: |{rest_of_line}|')

        try:
            self.current_token = rest_of_line[:(rest_of_line.index(' ') + 1)]
        except:
            self.current_token = rest_of_line
        print(f'Current token: |{self.current_token}|')

        # for now, just advance for every word
        # but first, we have to find the starting line index of our token which will be our self.currentIndex.
        token_start = self.current_index + len(self.current_token)
        if token_start >= len(self.file[self.line_number]):
            self.line_number += 1
            self.current_index = 0
        else:
            self.current_index = token_start
