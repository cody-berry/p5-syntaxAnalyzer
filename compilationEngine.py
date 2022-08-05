from jackTokenizer import *


class CompilationEngine:
    def __init__(self, filename, tokenizer):
        self.jack_tokenizer = tokenizer
        self.output = open(filename[:-5] + 'C.xml', 'w')
        self.indents = 1
        self.compile_class()

    # advances a token and checks if it is the correct one, if given a list sees if it is in the list
    def checkToken(self, advance, *token_and_type):
        if advance:
            self.jack_tokenizer.advance()

        wrote = False
        for token in token_and_type:
            if self.jack_tokenizer.current_token == token[0]:
                for i in range(0, self.indents):
                    self.output.write('\t')

                self.output.write(
                    '<' + token[1] + '> ' + token[0] + ' </' + token[1] + '>\n'
                )
                wrote = True

        if not wrote:
            raise ValueError('The current token is incorrect.')

    def compile_identifier(self, advance):
        if advance:
            self.jack_tokenizer.advance()


        if self.jack_tokenizer.token_type() == TokenType.IDENTIFIER:
            for i in range(0, self.indents):
                self.output.write('\t')

            self.output.write(
                '<identifier> ' + self.jack_tokenizer.current_token + ' </identifier>\n')
        else:
            print(self.jack_tokenizer.token_type())
            raise ValueError('The current token is incorrect.')

    def compile_class(self):
        self.output.write(
            '<class>\n'
        )

        self.checkToken(True, ['class', 'keyword'])
        self.compile_identifier(True)

        self.checkToken(True, ['{', 'symbol'])
        while True:
            try:
                self.indents += 1
                self.compile_class_var_dec()
                self.indents -= 1
            except ValueError:
                self.indents -= 1
                break

        while True:
            try:
                self.indents += 1
                self.compile_subroutine_dec()
                self.indents -= 1
            except ValueError:
                self.indents -= 1
                break
        self.checkToken(['}', 'symbol'])

        self.output.write(
            '</class>'
        )

    def compile_class_var_dec(self):
        self.output.write(
            '\t<classVarDec>\n'
        )

        self.checkToken(True, ['static', 'keyword'], ['field', 'keyword'])
        self.compile_type(True)
        self.compile_identifier(True)

        while True:
            try:
                self.checkToken(True, [',', 'symbol'])
                self.compile_identifier(True)
            except:
                break

        self.checkToken(False, [';', 'symbol'])

        self.output.write(
            '\t</classVarDec>\n'
        )

    def compile_type(self, advance):
        try:
            self.checkToken(advance, ['int', 'keyword'], ['char', 'keyword'], ['boolean', 'keyword'])
        except:
            self.compile_identifier(True)

    def compile_subroutine_dec(self):
        self.output.write(
            '\t<subroutineDec>\n'
        )

        self.checkToken(False, ['constructor', 'keyword'], ['function', 'keyword'], ['method', 'keyword'])
        try:
            self.checkToken(True, ['void', 'keyword'])
        except:
            self.compile_type(False)
        self.compile_identifier(True)
        self.checkToken(True, ['(', 'symbol'])
        self.indents += 1
        self.compile_parameter_list()
        self.indents -= 1
        self.checkToken(True, [')', 'symbol'])
        self.indents += 1
        self.compile_subroutine_body()
        self.indents -= 1

        self.output.write(
            '\t</subroutineDec>\n'
        )

    def compile_parameter_list(self):
        self.output.write(
            '\t\t<parameterList>\n'
        )

        try:
            self.compile_type(True)
            self.compile_identifier(True)
            while True:
                try:
                    self.checkToken(True, [',', 'symbol'])
                    self.compile_type(True)
                    self.compile_identifier(True)
                except:
                    break
        except:
            pass

        self.output.write(
            '\t\t</parameterList>\n'
        )
