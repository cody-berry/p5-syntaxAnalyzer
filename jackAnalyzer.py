from jackTokenizer import *
# from compilationEngine import *

tokenizer = JackTokenizer('Square/SquareGame.jack')
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
        case TokenType.SYMBOL:
            print(f'|{tokenizer.symbol()}|')
        case TokenType.KEYWORD:
            print(f'|{tokenizer.keyWord().name}|')

