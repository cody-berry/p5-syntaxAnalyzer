from jackTokenizer import *


class CompilationEngine:
    def __init__(self, filename, tokenizer):
        self.jack_tokenizer = tokenizer
        self.output = open(filename[:-5] + 'C.xml', 'w')
        self.compile_class()

    # advances a token and checks if it is the correct one, if given a list sees if it is in the list
    def checkToken(self, *token_and_type):
        self.jack_tokenizer.advance()
        for token in token_and_type:
            if self.jack_tokenizer.current_token == token[0]:
                self.output.write(
                    '<' + token[1] + '>' + token[0] + '</' + token[1] + '>\n'
                )

    def compile_class(self):
        self.output.write(
            '<class>\n'
        )

        self.checkToken(['class', 'keyword'])
        self.jack_tokenizer.advance()
        if self.jack_tokenizer.token_type() == TokenType.IDENTIFIER:
            self.output.write(
                '<identifier>' + self.jack_tokenizer.current_token + '</identifier>\n')

        self.checkToken(['{', 'symbol'])
        while True:
            try:
                self.compile_class_var_dec()
            except:
                break

        while True:
            try:
                self.compile_subroutine_var_dec()
            except:
                break
        self.checkToken(['}', 'symbol'])

        self.output.write(
            '</class>'
        )
