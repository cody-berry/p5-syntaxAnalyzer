from jackTokenizer import *
# from compilationEngine import *
import pathlib
files = []


for path in pathlib.Path(
        'Square').iterdir():  # iterate through all the files in the directory
    if path.__str__()[-4:] == 'jack':
        files.append(path.__str__())


for file in files:
    print(file + " —→ " + file[:-5] + 'T2.xml')
    tokenizer = JackTokenizer(file)
    tokens = open(file[:-5] + 'T2.xml', 'w')
    tokens.write('<tokens>\n')

    for line in tokenizer.file:
        print(line)

    while tokenizer.hasMoreTokens():
        tokenizer.advance()
        token_type = tokenizer.token_type()
        # print(token_type)
        match token_type:
            case TokenType.STRING_CONST:
                print(f'|{tokenizer.string_val()}|')
            case TokenType.INT_CONST:
                print(f'|{tokenizer.int_val()}|')
                tokens.write(f'<integerConstant> {tokenizer.int_val()} </integerConstant>\n')
            case TokenType.IDENTIFIER:
                print(f'|{tokenizer.identifier()}|')
                tokens.write(f'<identifier> {tokenizer.identifier()} </identifier>\n')
            case TokenType.SYMBOL:
                print(f'|{tokenizer.symbol()}|')
                tokens.write(f'<symbol> {tokenizer.symbol()} </symbol>\n')
            case TokenType.KEYWORD:
                print(f'|{tokenizer.keyWord().name.lower()}|')
                tokens.write(f'<keyword> {tokenizer.keyWord().name.lower()} </keyword>\n')
        print("---")

    tokens.write('</tokens>')

