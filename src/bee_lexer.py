import src.bee_token as tk

END_OF_FILE: str = '\0'


class Lexer:
    def __init__(self, input_string: str) -> None:
        self.input_string: str = input_string
        self.input_string += END_OF_FILE
        self.index: int = -1
        self.current_char: str = None
        self.tokens: list[tk.Token] = []

    def peek_char(self):
        self.index += 1
        self.current_char = self.input_string[self.index]

    def is_char(self, string: str) -> bool:
        return self.current_char in string

    def is_char_end_of_file(self) -> bool:
        return self.is_char(END_OF_FILE)

    def is_char_operator(self) -> bool:
        return self.is_char("+-*/")

    def is_char_seperator(self) -> bool:
        return self.is_char(",()")

    def peek_operator(self) -> tk.Token:

        str_: str = self.current_char

        self.peek_char()

        while not self.is_char_end_of_file() and self.is_char_operator():
            str_ += self.current_char
            self.peek_char()

        match str_:
            case '+':
                return tk.Token(tk.TokenKind.ADD_OP, '+')
            case '-':
                return tk.Token(tk.TokenKind.MIN_OP, '-')
            case '*':
                return tk.Token(tk.TokenKind.MUL_OP, '*')
            case '/':
                return tk.Token(tk.TokenKind.DIV_OP, '/')

    def peek_seperator(self) -> tk.Token:

        str_: str = self.current_char

        self.peek_char()

        while not self.is_char_end_of_file() and self.is_char_seperator():
            str_ += self.current_char
            self.peek_char()

        match str_:
            case '(':
                return tk.Token(tk.TokenKind.OpeningParenthesis, '(')
            case ')':
                return tk.Token(tk.TokenKind.ClosingParenthesis, ')')
            case ',':
                return tk.Token(tk.TokenKind.MUL_OP, ',')

    def peek_identifier(self) -> tk.Token:

        str_: str = self.current_char

        self.peek_char()

        while not self.is_char_end_of_file() and self.current_char.isalpha():
            str_ += self.current_char
            self.peek_char()

        return tk.Token(tk.TokenKind.Identifier, str_)

    def peek_numeric(self) -> tk.Token:

        str_: str = self.current_char

        self.peek_char()

        dot_count = 0

        while not self.is_char_end_of_file() and (self.current_char.isnumeric() or self.current_char == '.'):
            if self.current_char == '.':
                dot_count += 1

            if dot_count == 2:
                break
            else:
                str_ += self.current_char

            self.peek_char()

        if dot_count > 0:
            return tk.Token(tk.TokenKind.Float, str_)
        else:
            return tk.Token(tk.TokenKind.Integer, str_)

    def lex(self):
        self.peek_char()  # peek the "-1" token

        while self.current_char != END_OF_FILE:
            if self.is_char_operator():
                operator_token: tk.Token = self.peek_operator()
                self.tokens.append(operator_token)
            elif self.is_char_seperator():
                seperator_token: tk.Token = self.peek_seperator()
                self.tokens.append(seperator_token)
            elif self.current_char.isalpha():
                identifier_token: tk.Token = self.peek_identifier()
                self.tokens.append(identifier_token)
            elif self.current_char.isnumeric():
                numeric_token: tk.Token = self.peek_numeric()
                self.tokens.append(numeric_token)
            else:
                self.peek_char()

        self.tokens.append(tk.Token(tk.TokenKind.END, ''))
