from jackTokenizer import *


class CompilationEngine:
    def __init__(self, filename, tokenizer):
        self.jack_tokenizer = tokenizer
        self.output = open(filename[:-5] + 'C.xml', 'w')
        self.indents = 1
        self.compile_class()

    # advances a token and checks if it is the correct one, if given a list sees if it is in the list
    def checkToken(self, *token_and_type):
        self.jack_tokenizer.advance()

        wrote = False
        for token in token_and_type:
            if self.jack_tokenizer.current_token == token[0]:
                for i in range(0, self.indents):
                    self.output.write('\t')

                self.output.write(
                    '<' + token[1] + '>' + token[0] + '</' + token[1] + '>\n'
                )
                wrote = True

        if not wrote:
            raise ValueError('The current token is incorrect.')

    def compile_identifier(self):
        if self.jack_tokenizer.token_type() == TokenType.IDENTIFIER:
            for i in range(0, self.indents):
                self.output.write('\t')

            self.output.write(
                '<identifier>' + self.jack_tokenizer.current_token + '</identifier>\n')
        else:
            raise ValueError('The current token is incorrect.')

    def compile_class(self):
        self.output.write(
            '<class>\n'
        )

        self.checkToken(['class', 'keyword'])
        self.jack_tokenizer.advance()
        self.compile_identifier()

        self.checkToken(['{', 'symbol'])
        while True:
            try:
                self.indents += 1
                self.compile_class_var_dec()
                self.indents -= 1
            except:
                break

        while True:
            try:
                self.indents += 1
                self.compile_subroutine_dec()
                self.indents -= 1
            except:
                break
        self.checkToken(['}', 'symbol'])

        self.output.write(
            '</class>'
        )

    def compile_class_var_dec(self):
        self.output.write(
            '\t<classVarDec>\n'
        )

        self.checkToken(['static', 'keyword'], ['field', 'keyword'])
        self.compile_type()
        self.compile_identifier()

        while True:
            try:
                self.checkToken([',', 'symbol'])
                self.compile_identifier()
            except:
                break

        self.checkToken([';', 'symbol'])

        self.output.write(
            '\t</classVarDec>\n'
        )

    def compile_type(self):
        try:
            self.checkToken(['int', 'keyword'], ['char', 'keyword'], ['boolean', 'keyword'])
        except:
            self.compile_identifier()
