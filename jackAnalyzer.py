from jackTokenizer import *
from enum import Enum

# from compilationEngine import *

tokenizer = JackTokenizer('ExpressionLessSquare/SquareGame.jack')
for line in tokenizer.file:
    print(line + "|" + str(len(line)))

while tokenizer.hasMoreTokens():
    tokenizer.advance()
    print(tokenizer.token_type())
