from jackTokenizer import *
# from compilationEngine import *

tokenizer = JackTokenizer('Square/SquareGame.jack')
tokens = open('ExpressionLessSquare/SquareGameT2.xml', 'w')
tokens.write('<tokens>\n')


for line in tokenizer.file:
    print(line + "|" + str(len(line)))

while tokenizer.hasMoreTokens():
    tokenizer.advance()
    token_type = tokenizer.token_type()
    # print(token_type)
    match token_type:
        case TokenType.STRING_CONST:
            print(f'|{tokenizer.string_val()}|')
        case TokenType.INT_CONST:
            print(f'|{tokenizer.int_val()}|')
        case TokenType.IDENTIFIER:
            print(f'|{tokenizer.identifier()}|')
            tokens.write(f'<identifier> {tokenizer.identifier()} </identifier>\n')
        case TokenType.SYMBOL:
            print(f'|{tokenizer.symbol()}|')
            tokens.write(f'<symbol> {tokenizer.symbol()} </symbol>\n')
        case TokenType.KEYWORD:
            print(f'|{tokenizer.keyWord().name.lower()}|')
            tokens.write(f'<keyword> {tokenizer.keyWord().name.lower()} </keyword>\n')

tokens.write('</tokens>')

