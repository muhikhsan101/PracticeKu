# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, EOF, SPACE, MINUS = 'INTEGER', 'PLUS', 'EOF', 'SPACE', 'MINUS'

class Token(object):
    def __init__(self, type, value):
        # Token type: INTEGER, PLUS, or EOF
        self.type = type
        # Token value: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, '+', ' ' or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
        Token(INTEGER, 3)
        Token(PLUS, '+')
        """
        return 'Token({type}, {value})'.format(
        type=self.type,
        value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        #current token instance
        self.current_token = None

    def error(self):
        raise Exception('Error parsing input')

    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        text = self.text

        # is self.pos index past the end of the self.text ?
        # if so, then return EOF token because there is no more
        # input left to convert into tokens
        if self.pos > len(text) - 1:
            return Token(EOF, None)

        # get a character at the position self.pos and decide
        # what token to create based on the single character
        current_char = text[self.pos]

        # if the character is a digit then convert it to
        # integer, create an INTEGER token, increment self.pos
        # index to point to the next character after the digit,
        # and return the INTEGER token
        if current_char.isdigit():
            token = Token(INTEGER, int(current_char))
            self.pos += 1
            return token

        if current_char == '+':
            token = Token(PLUS, current_char)
            self.pos += 1
            return token

        if current_char == '-':
            token = Token(MINUS, current_char)
            self.pos += 1
            return token

        if current_char == ' ':
            token = Token(SPACE, current_char)
            self.pos += 1
            return token
        
        self.error()

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def skip_space(self):
        while self.current_token.type == SPACE:
            self.current_token = self.get_next_token()
        
    def expr(self):
        """expr -> INTEGER PLUS INTEGER"""
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        self.skip_space()
        # we expect the current token to be a single-digit integer
        left = self.current_token.value
        self.eat(INTEGER)
        while self.current_token.type == INTEGER:
            left = left * 10 + self.current_token.value
            self.current_token = self.get_next_token()

        self.skip_space()
        # we expect the current token to be a '+' token
        op = self.current_token
        try:
            self.eat(PLUS)
        except Exception:
            self.eat(MINUS)

        self.skip_space()
        # we expect the current token to be a single-digit integer
        right = self.current_token.value
        self.eat(INTEGER)
        while self.current_token.type == INTEGER:
            right = right * 10 + self.current_token.value
            self.current_token = self.get_next_token()
            
        # after the above call the self.current_token is set to
        # EOF token

        # at this point INTEGER PLUS INTEGER sequence of tokens
        # has been successfully found and the method can just
        # return the result of adding two integers, thus
        # effectifely interpreting client input
        if (op.type == PLUS):
            result = left + right
        else:
            result = left - right
            
        return result


def main():
    while True:
        try:
            # To run under Python3 replace 'raw_input' call
            # with 'input'
            text = raw_input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
