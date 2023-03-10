import src.bee_token
import enum


class OperatorType(enum.IntEnum):
    Addition = enum.auto()
    Subtraction = enum.auto()
    Multiplication = enum.auto()
    Division = enum.auto()


class Value:
    """value node"""

    def __init__(self, value: int | float):
        self.value = value

    def __str__(self):
        return str(self.value)


class Negate:
    """negate node"""

    def __init__(self, value: 'Operator | Value'):
        self.value = value

    def __str__(self):
        return f"(-{str(self.value)})"


class Operator:
    """operator node"""

    def __init__(self, type: OperatorType, left: 'Operator | Value | Negate', right: 'Operator | Value | Negate'):
        self.type = type
        self.left = left
        self.right = right

    def __str__(self):
        str_ = "("
        str_ += f"{self.left} "
        match self.type:
            case OperatorType.Addition:
                str_ += "+ "
            case OperatorType.Subtraction:
                str_ += "- "
            case OperatorType.Multiplication:
                str_ += "* "
            case OperatorType.Division:
                str_ += "/ "

        str_ += f"{self.right})"

        return str_


class Parser:
    """parser"""
    """
    The Grammar:
    expression -> term {-|+ term}
    term       -> factor {*|/ factor}
    factor     -> integer | float | (expression) | -factor
    """

    def __init__(self, tokens: list[src.bee_token.Token]):
        self.tokens: list[src.bee_token.Token] = tokens
        self.current_token: src.bee_token.Token = tokens[0]
        self.index: int = 0
        self.start_node = self.parse_expression()

    def scan_token(self):
        self.index += 1
        self.current_token = self.tokens[self.index]

    def parse_expression(self):
        left_term = self.parse_term()
        while True:
            if self.current_token.kind == src.bee_token.TokenKind.Plus:
                self.scan_token()
                right_term = self.parse_term()
                if right_term is None:
                    return None
                left_term = Operator(OperatorType.Addition, left_term, right_term)
            elif self.current_token.kind == src.bee_token.TokenKind.Minus:
                self.scan_token()
                right_term = self.parse_term()
                if right_term is None:
                    return None
                left_term = Operator(OperatorType.Subtraction, left_term, right_term)
            else:
                return left_term

    def parse_term(self):
        left_factor = self.parse_factor()
        while True:
            if self.current_token.kind == src.bee_token.TokenKind.Asterisk:
                self.scan_token()
                right_factor = self.parse_factor()
                if right_factor is None:
                    return None
                left_factor = Operator(OperatorType.Multiplication, left_factor, right_factor)
            elif self.current_token.kind == src.bee_token.TokenKind.ForwardSlash:
                self.scan_token()
                right_factor = self.parse_factor()
                if right_factor is None:
                    return None
                left_factor = Operator(OperatorType.Division, left_factor, right_factor)
            else:
                return left_factor

    def parse_factor(self):
        if self.current_token.kind == src.bee_token.TokenKind.Integer:
            temp_ = Value(int(self.current_token.string))
            self.scan_token()
            return temp_
        elif self.current_token.kind == src.bee_token.TokenKind.Float:
            temp_ = Value(float(self.current_token.string))
            self.scan_token()
            return temp_
        elif self.current_token.kind == src.bee_token.TokenKind.OpenParenthesis:
            self.scan_token()
            sub_expression = self.parse_expression()
            if sub_expression is None:
                return None
            if self.current_token.kind == src.bee_token.TokenKind.ClosingParenthesis:
                self.scan_token()
                return sub_expression
            else:
                return None
        elif self.current_token.kind == src.bee_token.TokenKind.Minus:
            self.scan_token()
            return Negate(self.parse_factor())
        else:
            return None
