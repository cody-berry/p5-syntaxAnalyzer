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
    # if given a list sees if it is in the list
    def check_token(self, advance, tokens):
        if advance:
            self.advance()

        wrote = False
        for token in tokens:
            print(token)
            if self.tokenizer.current_token == token:
                for i in range(0, self.indents):
                    self.output.write('\t')

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
                self.output.write('\t')

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

        self.output.write('</class\n')



