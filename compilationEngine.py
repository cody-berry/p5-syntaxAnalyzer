from jackTokenizer import *


class CompilationEngine:
    def __init__(self, filename, tokenizer):
        self.tokenizer = tokenizer
        self.output = open(filename[:-5] + 'C.xml', 'w')
        self.indents = 1
        self.compile_class()

    # advances
    def advance(self):
        if self.tokenizer.hasMoreTokens():
            print('advancing')
            self.tokenizer.advance()
            print(self.tokenizer.current_token + '|')

    # advances a token and checks if it is the correct one,
    # if given a list sees if it is in the list of tokens, literally 'tokens'
    def check_token(self, advance, tokens):
        if advance:
            self.advance()

        wrote = False
        for token in tokens:
            print(token)
            if self.tokenizer.current_token == token:
                for i in range(0, self.indents):
                    self.output.write('  ')

                self.output.write(
                    '<' + self.tokenizer.token_type().name.lower() + '> ' + token +
                    ' </' + self.tokenizer.token_type().name.lower() + '>\n'
                )
                wrote = True

        if not wrote:
            raise ValueError('The current token is incorrect.')

    def compile_identifier(self, advance):
        if advance:
            self.advance()

        if self.tokenizer.token_type() == TokenType.IDENTIFIER:
            for i in range(0, self.indents):
                self.output.write('  ')

            self.output.write(
                '<identifier> ' + self.tokenizer.current_token + ' </identifier>\n')
        else:
            print(self.tokenizer.token_type())
            raise ValueError('The current token is incorrect.')

    # grammar: 'class' identifier '{' classVarDec* subroutineDec* '}'
    def compile_class(self):
        self.output.write('<class>\n')

        # 'class'
        self.check_token(True, ['class'])

        # identifier
        self.compile_identifier(True)

        # '{'
        self.check_token(True, ['{'])

        self.advance()
        # classVarDec*
        while self.tokenizer.current_token in ['static', 'field']:
            self.compile_class_var_dec()
            self.advance()

        # subroutineVarDec*
        while self.tokenizer.current_token in ['constructor', 'function', 'method']:
            self.compile_subroutine_dec()
            self.advance()

        # '}'
        self.check_token(False, ['}'])

        self.output.write('</class\n')

    # grammar: 'static'/'field' type varName *(',' varName) ';'
    def compile_class_var_dec(self):
        self.output.write('  <classVarDec>\n')
        self.indents += 1

        # 'static'/'field'
        self.check_token(False, ['static', 'field'])

        # type, which does not end advanced
        self.compile_type(True)

        # varName
        self.compile_identifier(True)

        self.advance()
        # *( and checks if the token is a comma
        while self.tokenizer.current_token == ',':
            self.check_token(False, ',')

            # varName
            self.compile_identifier(True)

            # advance so that we're ready to check if the current token is a comma again
            self.advance()

        # ';'
        self.check_token(False, ';')

        self.indents -= 1
        self.output.write('  </classVarDec>\n')

    # grammar: 'int', 'boolean', 'char', or an identifier. sometimes you'll
    # want to advance, other times you won't. for example, if you just called
    # check_token() or compile_identifier(), you'll want to advance. if you
    # just did an advance() or you just finished an asterisk loop or question
    # if-else statement.
    def compile_type(self, advance=True):
        for i in range(0, self.indents):
            # two spaces as a substitute for a tab. useful for testing purposes
            # because all test cases use two spaces for indentations too.
            self.output.write('  ')

        self.output.write('<type>\n')
        self.indents += 1

        # advance if we want to advance
        if advance:
            self.advance()

        # 'int', 'boolean', or 'char' with the if-else statement
        if self.tokenizer.current_token in ['int', 'boolean', 'char']:
            self.check_token(False, ['int', 'boolean', 'char'])
        else:  # and otherwise it's className, an identifier.
            self.compile_identifier(False)

        self.indents -= 1

        for i in range(0, self.indents):
            # two spaces as a substitute for a tab. useful for testing purposes
            # because all test cases use two spaces for indentations too.
            self.output.write('  ')
        self.output.write('</type>\n')

    # grammar: constructor/function/method void/type subroutineName
    # '(' parameterList ')' subroutineBody
    def compile_subroutine_dec(self):
        self.output.write('  <subroutineDec>\n')
        self.indents += 1

        # constructor/function/method. note that because we just checked that it
        # was a constructor, functon, or method, we don't need to advance.
        self.check_token(False, ['constructor', 'function', 'method'])

        # 'void' or a type.
        self.tokenizer.advance()
        if self.tokenizer.current_token == 'void':
            self.check_token(False, ['void'])
        else:
            # this is an 'or' case where we need to check if it's 'void' or a type.
            # because of this, we've already advanced, so we shouldn't advance.
            # if we did advance, it would still pass the tests if the code worked
            # because it would have an identifier right after.
            self.compile_type(False)

        # subroutineName, which is the equivalent of an identifier. we advance
        self.compile_identifier(True)

        # '(', the symbol
        self.check_token(True, ['('])

        # parameterList, a function. based on the formula, it ends advanced to
        # the next token
        self.compile_parameter_list()

        # read the last comment to show description of why we don't advance for our ')'
        self.check_token(False, [')'])

        # subroutineBody, the function
        self.compile_subroutine_body()

        self.indents -= 1
        self.output.write('  <subroutineDec>\n')

    # grammar: ?(type varname *(',' type varName))
    def compile_parameter_list(self):
        self.output.write('    <parameterList>\n')
        self.indents += 1

        # ?(type
        self.advance()
        if self.tokenizer.token_type() in [TokenType.KEYWORD, TokenType.IDENTIFIER]:
            self.compile_type(False)

            # varName
            self.compile_identifier(True)

            # *(','
            self.tokenizer.advance()
            while self.tokenizer.current_token == ',':
                self.check_token(False, [','])

                # type
                self.compile_type(True)

                # varName
                self.compile_identifier(True)

                # prepare for the next iteration of this
                self.tokenizer.advance()

        self.indents -= 1
        self.output.write('    <parameterList>\n')

    # grammar: '{' varDec* statements '}'
    def compile_subroutine_body(self):
        self.output.write('    <subroutineBody>\n')
        self.indents += 1

        # '{'
        self.check_token(True, ['{'])

        # varDec*
        self.tokenizer.advance()
        while self.tokenizer.current_token == 'var':
            self.compile_var_dec()
            self.tokenizer.advance()

        # statements
        self.compile_statements()

        # '}'
        self.check_token(False, ['}'])

        self.indents -= 1
        self.output.write('    <subroutineBody>\n')

    # grammar: 'var' type varName *(',' varName) ';'. the only time this is called
    # we have already started advance()
    def compile_var_dec(self):
        self.output.write('      <varDec>\n')
        self.indents += 1

        # 'var'
        self.check_token(False, ['var'])

        # type
        self.compile_type(True)

        # varName
        self.compile_identifier(True)

        # grammar: repeat ',' varName
        self.advance()
        while self.tokenizer.current_token == ',':
            self.check_token(False, [','])
            self.compile_identifier(True)
            self.advance()

        self.check_token(False, [';'])

        self.indents -= 1
        self.output.write('      <varDec>\n')

    # grammar: statement*
    def compile_statements(self):
        for i in range(0, self.indents):
            self.output.write('  ')
        self.output.write('<statements>')
        self.indents += 1

        # not only does compile_statement() write down everything needed for a statement,
        # but it returns true if there is a statement and false if there isn't. it also takes care of advancing
        # by itself because of the formula of the if statement, ending right after the optional else statement
        # meaning that all other statements have advanced after.
        while self.compile_statement():
            pass

        self.indents -= 1
        for i in range(0, self.indents):
            self.output.write('  ')
        self.output.write('<statements>')


