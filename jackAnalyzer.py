from jackTokenizer import *
# from compilationEngine import *

tokenizer = JackTokenizer('ExpressionLessSquare/Main.jack')
for line in tokenizer.file:
    print(line + "|" + str(len(line)))

while tokenizer.hasMoreTokens():
    tokenizer.advance()
