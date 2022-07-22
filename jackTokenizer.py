from enum import Enum


class TokenType(Enum):
    KEYWORD = 0
    SYMBOL = 1
    IDENTIFIER = 2
    INT_CONST = 3
    STRING_CONST = 4


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

            line = line[:-1].strip(' ')

            if (len(line) > 0) and (line[0] != '/'):
                self.file.append(line)

    def hasMoreTokens(self):
        return not ((self.line_number >= len(self.file) - 1) and (
                self.current_index + len(self.current_token) >= (
            len(self.file[self.line_number]))))

    def advance(self):

        # print(f'Token starting index: |{self.current_index}|')

        rest_of_line = self.file[self.line_number][self.current_index:].strip(' ')
        print(f'Rest of line: |{rest_of_line}|')

        possible_token_ending_indices = [len(rest_of_line)]

        try:
            possible_token_ending_indices.append(rest_of_line.index(' ') + 1)
        except:
            pass

        for token_breaker in ['+', '-', '~', '*', '/', '&', '|', '<', '>', '=',
                              '}', '{', ')', '(', '[', ']', '.', ',', ';']:
            try:
                index = rest_of_line.index(token_breaker)
                if index > 0:
                    possible_token_ending_indices.append(index)
                else:
                    possible_token_ending_indices.append(1)
            except:
                pass

        if len(possible_token_ending_indices) > 1:
            for i in range(0, len(possible_token_ending_indices) - 1):
                possible_token_ending_indices[0] = min(
                    possible_token_ending_indices[0],
                    possible_token_ending_indices[i + 1])

        token_end = possible_token_ending_indices[0]

        self.current_token = rest_of_line[:token_end]

        # if self.current_token[0] == "\"":
        #     self.current_token = rest_of_line[:rest_of_line.index("\"") + 1]

        # for now, just advance for every word
        # but first, we have to find the starting line index of our token which will be our self.currentIndex.
        token_start = self.current_index + len(self.current_token)
        if token_start >= len(self.file[self.line_number]):
            self.line_number += 1
            self.current_index = 0
        else:
            self.current_index = token_start

        if self.current_token:
            if self.current_token[-1] == ' ':
                self.current_token = self.current_token[:-1]

        print(f'Current token: |{self.current_token}|')

    def token_type(self):
        if self.current_token in ['class', 'constructor', 'function', 'method',
                                  'field', 'static', 'var', 'int', 'char',
                                  'boolean', 'void', 'true', 'false', 'null',
                                  'this', 'let', 'do', 'if', 'else', 'while',
                                  'return']:
            return TokenType.KEYWORD
        if self.current_token in ['{', '}', '(', ')', '[', ']', '.', ',', ';',
                                  '+', '-', '*', '/', '&', '|', '<', '>', '=',
                                  '~']:
            return TokenType.SYMBOL
        if self.current_token[0] in ['0', '1', '2', '3', '4', '5', '6', '7',
                                     '8', '9']:
            return TokenType.INT_CONST
        if self.current_token[0] == ["\""]:
            self.advance()  # like this we're skipping the first token (") so that the next token i our actual string constant
            return TokenType.STRING_CONST
        else:
            return TokenType.IDENTIFIER
