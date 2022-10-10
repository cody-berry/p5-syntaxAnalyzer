from jackTokenizer import *
from compilationEngine import *
file = 'ExpressionLessSquare/Main.jack'

# don't even need this anymore, this is just for testing purposes
#
# for file in files:
#     print(file + " —→ " + file[:-5] + 'T2.xml')
#     tokenizer = JackTokenizer(file)
#     tokens = open(file[:-5] + 'T2.xml', 'w')
#     tokens.write('<tokens>\n')
#
#     for line in tokenizer.file:
#         print(line)
#
#     # code below is for testing JackTokenizer, but we don't need that anymore
#     #
#     # while tokenizer.hasMoreTokens():
#     #     tokenizer.advance()
#     #     token_type = tokenizer.token_type()
#     #     # print(token_type)
#     #     match token_type:
#     #         case TokenType.STRING_CONST:
#     #             # print(f'|{tokenizer.string_val()}|🌟')
#     #             tokens.write(f'<stringConstant> {tokenizer.string_val()} </stringConstant>\n')
#     #         case TokenType.INT_CONST:
#     #             print(f'|{tokenizer.int_val()}|')
#     #             tokens.write(f'<integerConstant> {tokenizer.int_val()} </integerConstant>\n')
#     #         case TokenType.IDENTIFIER:
#     #             print(f'|{tokenizer.identifier()}|')
#     #             tokens.write(f'<identifier> {tokenizer.identifier()} </identifier>\n')
#     #         case TokenType.SYMBOL:
#     #             print(f'|{tokenizer.symbol()}|')
#     #             tokens.write(f'<symbol> {tokenizer.symbol()} </symbol>\n')
#     #         case TokenType.KEYWORD:
#     #             print(f'|{tokenizer.keyWord().name.lower()}|')
#     #             tokens.write(f'<keyword> {tokenizer.keyWord().name.lower()} </keyword>\n')
#     #     print("---")
#
#     tokens.write('</tokens>')
tokenizer = JackTokenizer(file)
compileEngine = CompilationEngine(file, tokenizer)







