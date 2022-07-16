from jackTokenizer import *
# from compilationEngine import *

tokenizer = JackTokenizer('ExpressionLessSquare/Main.jack')
for line in tokenizer.file:
    print(line)

print(tokenizer.hasMoreTokens())


# file = open('ArrayTest/Main.jack', 'r')
#
#
# for line in file:
#     # this way no line will include the ending newline
#     line = line[:-1]
#
#     print(line)
