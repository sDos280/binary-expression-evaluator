import src.bee_token


class Tokenizer:
    def __init__(self, input_string: str) -> None:
        self.input_string: str = input_string
        self.tokens: list[Token] = []

    def tokenize(self):
        index: int = 0
        while index < len(self.input_string):
            if self.input_string[index] == ' ':  # check for a white space, if true, bump the index
                index += 1

            elif self.input_string[index].isdigit():  # check if an integer, if true, check if that number is integer or float
                temp: str = ""
                dot_count: int = 0

                while index < len(self.input_string) and (self.input_string[index].isdigit() or self.input_string[index] == '.'):  # check if a digit or a dot
                    if self.input_string[index] == '.':
                        dot_count += 1
                    if dot_count == 2:  # a float literal can only contain one dot
                        break

                    temp += self.input_string[index]
                    index += 1

                if dot_count == 0:  # an integer
                    self.tokens.append(src.bee_token.Token(src.bee_token.TokenKind.Integer, temp))
                else:  # a float
                    self.tokens.append(src.bee_token.Token(src.bee_token.TokenKind.Float, temp))

            elif self.input_string[index] in "+-*/":  # check for operator, if true add the specific operator
                if self.input_string[index] in "+":
                    self.tokens.append(src.bee_token.Token(src.bee_token.TokenKind.Plus, '+'))
                elif self.input_string[index] in "-":
                    self.tokens.append(src.bee_token.Token(src.bee_token.TokenKind.Minus, '-'))
                elif self.input_string[index] in "*":
                    self.tokens.append(src.bee_token.Token(src.bee_token.TokenKind.Asterisk, '*'))
                elif self.input_string[index] in "/":
                    self.tokens.append(src.bee_token.Token(src.bee_token.TokenKind.ForwardSlash, '/'))

                index += 1

            elif self.input_string[index] in "()":   # check for open/closing parenthesis, if true add the specific parenthesis
                if self.input_string[index] in "(":
                    self.tokens.append(src.bee_token.Token(src.bee_token.TokenKind.OpenParenthesis, '('))
                elif self.input_string[index] in ")":
                    self.tokens.append(src.bee_token.Token(src.bee_token.TokenKind.ClosingParenthesis, ')'))

                index += 1

            else:  # the character is unknown
                raise SyntaxError(f"the character \'{self.input_string[index]}\' is unknown")

        # add end token
        self.tokens.append(src.bee_token.Token(src.bee_token.TokenKind.END, ""))
