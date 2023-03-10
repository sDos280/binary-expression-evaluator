import src.bee_token
import enum
import math


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

    def eval(self):
        return self.value


class Negate:
    """negate node"""

    def __init__(self, value: 'Operator | Value | Negate | Function'):
        self.value = value

    def __str__(self):
        return f"(-{str(self.value)})"

    def eval(self):
        return -self.value.eval()

class Operator:
    """operator node"""

    def __init__(self, type: OperatorType, left: 'Operator | Value | Negate | Function', right: 'Operator | Value | Negate | Function'):
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

    def eval(self):
        match self.type:
            case OperatorType.Addition:
                return self.left.eval() + self.right.eval()
            case OperatorType.Subtraction:
                return self.left.eval() - self.right.eval()
            case OperatorType.Multiplication:
                return self.left.eval() * self.right.eval()
            case OperatorType.Division:
                return self.left.eval() / self.right.eval()

class Function:
    """function node"""

    def __init__(self, name: str, expressions: list['Operator | Value | Negate | Function']):
        self.name = name
        self.expressions = expressions

    def __str__(self):
        str_ = f"{self.name}("
        if len(self.expressions) == 1:
            str_ += f"{self.expressions[0]})"
        else:
            for expression in self.expressions:
                str_ += f"{expression}, "

        str_ = str_[:-2]
        str_ += ")"

        return str_

    def eval(self):
        match self.name:
            case "sin":
                if len(self.expressions) == 1:
                    return math.sin(self.expressions[0].eval())
                else:
                    raise SyntaxError(f"too much arguments")
            case "cos":
                if len(self.expressions) == 1:
                    return math.cos(self.expressions[0].eval())
                else:
                    raise SyntaxError(f"too much arguments")

            case _:
                raise SyntaxError(f"the function \"{self.name}\" isn't supported")

class Parser:
    """parser"""
    """
    The Grammar:
    expression -> term {"-"|"+" term}
    term       -> factor {"*"|"/" factor}
    factor     -> integer | float | "(" expression ")" | "-" factor | "function_name" "(" [expression ["," expression]]* ")"
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
        elif self.current_token.kind == src.bee_token.TokenKind.Identifier:
            name = self.current_token.string
            self.scan_token()
            expressions: list['Operator | Value | Negate'] = []
            if self.current_token.kind == src.bee_token.TokenKind.OpenParenthesis:
                self.scan_token()
                sub_expression = self.parse_expression()
                expressions.append(sub_expression)

                while sub_expression is not None and self.current_token.kind == src.bee_token.TokenKind.Comma:
                    self.scan_token()
                    sub_expression = self.parse_expression()
                    if sub_expression is not None:
                        expressions.append(sub_expression)

                if self.current_token.kind == src.bee_token.TokenKind.ClosingParenthesis:
                    self.scan_token()
                    return Function(name, expressions)
                else:
                    return None
            else:
                return None
        else:
            return None
