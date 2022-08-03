class CompilationEngine:
    def __init__(self, filename, tokenizer):
        self.jack_tokenizer = tokenizer
        self.output = open(filename[:-5] + 'C.xml', 'w')
        self.compile_class()

    # advances a token and checks if it is the correct one, if given a list sees if it is in the list
    def checkToken(self, *correct_token_and_token_type):
        self.jack_tokenizer.advance()
        for token in correct_token_and_token_type:
            if self.jack_tokenizer.current_token == token[0]:
                self.output.write(
                    '<' + token[1] + '>' + token[0] + '</' + token[1] + '>\n'
                )

    def compile_class(self):
        self.output.write(
            '<class\n>'
        )

        self.output.write(
            '</class\n>'
        )
