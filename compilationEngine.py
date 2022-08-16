from jackTokenizer import *


class CompilationEngine:
    def __init__(self, filename, tokenizer):
        self.jack_tokenizer = tokenizer
        self.output = open(filename[:-5] + 'C.xml', 'w')
        self.indents = 1
        self.compile_class()

    # advances a token and checks if it is the correct one, if given a list sees if it is in the list
    def check_token(self, advance, *token_and_type):
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

        self.check_token(True, ['class', 'keyword'])
        self.compile_identifier(True)

        self.check_token(True, ['{', 'symbol'])
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
        self.check_token(['}', 'symbol'])

        self.output.write(
            '</class>'
        )

    def compile_class_var_dec(self):
        self.output.write(
            '\t<classVarDec>\n'
        )

        self.check_token(True, ['static', 'keyword'], ['field', 'keyword'])
        self.compile_type(True)
        self.compile_identifier(True)

        while True:
            try:
                self.check_token(True, [',', 'symbol'])
                self.compile_identifier(True)
            except:
                break

        self.check_token(False, [';', 'symbol'])

        self.output.write(
            '\t</classVarDec>\n'
        )

    def compile_type(self, advance):
        try:
            self.check_token(advance, ['int', 'keyword'], ['char', 'keyword'],
                             ['boolean', 'keyword'])
        except:
            self.compile_identifier(False)

    def compile_subroutine_dec(self):
        self.output.write(
            '\t<subroutineDec>\n'
        )

        self.check_token(False, ['constructor', 'keyword'],
                         ['function', 'keyword'], ['method', 'keyword'])
        try:
            self.check_token(True, ['void', 'keyword'])
        except:
            self.compile_type(False)
        self.compile_identifier(True)
        self.check_token(True, ['(', 'symbol'])
        self.indents += 1
        self.compile_parameter_list()
        self.indents -= 1
        self.check_token(False, [')', 'symbol'])
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
                    self.check_token(True, [',', 'symbol'])
                    self.compile_type(True)
                    self.compile_identifier(True)
                except:
                    break
        except:
            pass

        self.output.write(
            '\t\t</parameterList>\n'
        )

    def compile_subroutine_body(self):
        self.output.write(
            '\t\t<subroutineBody>\n'
        )

        self.check_token(True, ['{', 'symbol'])
        while True:
            try:
                self.indents += 1
                self.compile_var_dec()
                self.indents -= 1
            except:
                self.indents -= 1
                break
        self.indents += 1
        self.compile_statements()
        self.indents -= 1
        self.check_token(True, ['}', 'symbol'])

        self.output.write(
            '\t\t</subroutineBody>\n'
        )

    def compile_var_dec(self):
        self.output.write(
            '\t\t\t<varDec>\n'
        )

        self.check_token(True, ['var', 'keyword'])
        self.compile_type(True)
        self.compile_identifier(True)
        while True:
            try:
                self.check_token(True, [',', 'symbol'])
                self.compile_identifier(True)
            except:
                break
        self.check_token(False, [';', 'symbol'])

        self.output.write(
            '\t\t\t</varDec>\n'
        )

    def compile_statements(self):
        for indentNum in range(0, self.indents):
            self.output.write('\t')

        self.output.write(
            '<statements>\n'
        )

        while True:
            try:
                self.indents += 1
                self.compile_statement()
                self.indents -= 1
            except:
                self.indents -= 1
                break

        for indentNum in range(0, self.indents):
            self.output.write('\t')
        self.output.write(
            '</statements>\n'
        )

    def compile_statement(self):
        try:
            self.compile_let()
        except:
            try:
                self.compile_if()
            except:
                try:
                    self.compile_do()
                except:
                    try:
                        self.compile_while()
                    except:
                        self.compile_return()

    def compile_let(self):
        for indentNum in range(0, self.indents):
            self.output.write('\t')
        self.output.write(
            '<letStatement>\n'
        )

        self.check_token(False, ['let', 'keyword'])
        self.compile_identifier(True)

        try:
            self.check_token(True, ['[', 'symbol'])
            self.compile_expression()
            self.check_token(True, [']', 'symbol'])
        except:
            self.check_token(False, ['=', 'symbol'])
            pass
        else:
            self.check_token(True, ['=', 'symbol'])

        self.compile_expression()
        self.check_token(True, [';', 'symbol'])

        for indentNum in range(0, self.indents):
            self.output.write('\t')
        self.output.write(
            '</letStatement>\n'
        )

