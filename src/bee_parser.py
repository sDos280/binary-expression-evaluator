from __future__ import annotations
import src.bee_token as tk
import enum
import math


class BinaryOpKind(enum.Enum):
    """Binary Operator Type"""
    Addition = enum.auto()
    Subtraction = enum.auto()
    Multiplication = enum.auto()
    Division = enum.auto()


class UnaryOpKind(enum.Enum):
    """Unary Operator Type"""
    Negate = enum.auto()
    Plus = enum.auto()


class Number:

    def __init__(self, value: int | float):
        self.value: int | float = value

    def __str__(self):
        return str(self.value)

    def eval(self):
        return self.value


class Identifier:
    def __init__(self, name: str):
        self.name: str = name

    def __str__(self):
        return self.name


class UnaryOp:

    def __init__(self, kind: UnaryOpKind, value: BinaryOp | UnaryOp | Number):
        self.kind: UnaryOpKind = kind
        self.value: BinaryOp | UnaryOp | Number = value

    def __str__(self):
        match self.kind:
            case UnaryOpKind.Plus:
                return f"(+{str(self.value)})"
            case UnaryOpKind.Negate:
                return f"(-{str(self.value)})"

    def eval(self):
        match self.kind:
            case UnaryOpKind.Plus:
                return self.value.eval()
            case UnaryOpKind.Negate:
                return -self.value.eval()


class BinaryOp:
    def __init__(self, kind: BinaryOpKind, left: BinaryOp | UnaryOp | Number, right: BinaryOp | UnaryOp | Number):
        self.kind: BinaryOpKind = kind
        self.left: BinaryOp | UnaryOp | Number = left
        self.right: BinaryOp | UnaryOp | Number = right

    def __str__(self):
        str_ = "("
        str_ += f"{self.left} "
        match self.kind:
            case BinaryOpKind.Addition:
                str_ += "+ "
            case BinaryOpKind.Subtraction:
                str_ += "- "
            case BinaryOpKind.Multiplication:
                str_ += "* "
            case BinaryOpKind.Division:
                str_ += "/ "

        str_ += f"{self.right})"

        return str_

    def eval(self):
        match self.kind:
            case BinaryOpKind.Addition:
                return self.left.eval() + self.right.eval()
            case BinaryOpKind.Subtraction:
                return self.left.eval() - self.right.eval()
            case BinaryOpKind.Multiplication:
                return self.left.eval() * self.right.eval()
            case BinaryOpKind.Division:
                return self.left.eval() / self.right.eval()


class Function:
    """function node"""

    def __init__(self, name: str, expressions: list[BinaryOp | UnaryOp | Number]):
        self.name: str = name
        self.expressions: list[BinaryOp | UnaryOp | Number] = expressions

    def __str__(self):
        str_ = f"{self.name}("
        if len(self.expressions) != 0:
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
                    raise SyntaxError(f"too much/few arguments")
            case "cos":
                if len(self.expressions) == 1:
                    return math.cos(self.expressions[0].eval())
                else:
                    raise SyntaxError(f"too much/few arguments")

            case _:
                raise SyntaxError(f"the function \"{self.name}\" isn't supported")


class Parser:
    def __init__(self, tokens: list[tk.Token]):
        self.tokens: list[tk.Token] = tokens
        self.current_token: tk.Token = None
        self.index: int = -1
        self.AST: BinaryOp | UnaryOp | Number = None

    def peek_token(self):
        self.index += 1
        self.current_token = self.tokens[self.index]

    def is_token_kind(self, kind: tk.TokenKind) -> BinaryOp | UnaryOp | Number | Identifier:
        return self.current_token.kind == kind

    def peek_primary_expression(self):
        if self.is_token_kind(tk.TokenKind.Integer):
            number: Number = Number(int(self.current_token.string))

            self.peek_token()  # peek number token

            return number
        elif self.is_token_kind(tk.TokenKind.Float):
            number: Number = Number(float(self.current_token.string))

            self.peek_token()  # peek number token

            return number
        elif self.is_token_kind(tk.TokenKind.Identifier):
            identifier: Identifier = Identifier(self.current_token.string)

            self.peek_token()  # peek identifier token

            return identifier
        elif self.is_token_kind(tk.TokenKind.OpeningParenthesis):
            self.peek_token()  # peek open parenthesis token

            expression: BinaryOp | UnaryOp | Number = self.peek_expression()

            if not self.is_token_kind(tk.TokenKind.ClosingParenthesis):
                raise SyntaxError("expect a closing parenthesis")
            else:
                self.peek_token()  # peek close parenthesis token

            return expression

    def peek_postfix_expression(self):
        primary_expression: BinaryOp | UnaryOp | Number | Identifier = self.peek_primary_expression()
        if isinstance(primary_expression, Identifier):  # a function call

            expressions: list[BinaryOp | UnaryOp | Number] = []
            if not self.is_token_kind(tk.TokenKind.OpeningParenthesis):
                raise SyntaxError("An opening parenthesis is needed for function call")

            self.peek_token()  # peek opening parenthesis token

            if self.is_token_kind(tk.TokenKind.ClosingParenthesis):
                self.peek_token()  # peek closing parenthesis token
                return Function(primary_expression.name, [])

            while not self.is_token_kind(tk.TokenKind.END):
                expression: BinaryOp | UnaryOp | Number = self.peek_expression()

                expressions.append(expression)

                if self.is_token_kind(tk.TokenKind.Comma):
                    self.peek_token()  # peek comma token

                if self.is_token_kind(tk.TokenKind.ClosingParenthesis):
                    self.peek_token()  # peek closing parenthesis token
                    break

            return Function(primary_expression.name, expressions)
        else:
            return primary_expression

    def peek_unary_expression(self) -> BinaryOp | UnaryOp | Number:
        if self.is_token_kind(tk.TokenKind.ADD_OP):
            self.peek_token()  # peek the add op token

            postfix_expression: BinaryOp | UnaryOp | Number = self.peek_postfix_expression()

            return UnaryOp(UnaryOpKind.Plus, postfix_expression)

        elif self.is_token_kind(tk.TokenKind.MIN_OP):
            self.peek_token()  # peek the min op token

            postfix_expression: BinaryOp | UnaryOp | Number = self.peek_postfix_expression()

            return UnaryOp(UnaryOpKind.Negate, postfix_expression)

        postfix_expression: BinaryOp | UnaryOp | Number = self.peek_postfix_expression()

        return postfix_expression

    def peek_multiplicative_expression(self) -> BinaryOp | UnaryOp | Number:
        unary_expression: BinaryOp | UnaryOp | Number = self.peek_unary_expression()

        while True:
            if self.is_token_kind(tk.TokenKind.MUL_OP):
                self.peek_token()  # peek the mul op token

                sub_unary_expression: BinaryOp | UnaryOp | Number = self.peek_unary_expression()

                unary_expression = BinaryOp(BinaryOpKind.Multiplication, unary_expression, sub_unary_expression)

            elif self.is_token_kind(tk.TokenKind.DIV_OP):
                self.peek_token()  # peek the div op token

                sub_unary_expression: BinaryOp | UnaryOp | Number = self.peek_unary_expression()

                unary_expression = BinaryOp(BinaryOpKind.Division, unary_expression, sub_unary_expression)
            else:
                return unary_expression

    def peek_additive_expression(self) -> BinaryOp | UnaryOp | Number:
        multiplicative_expression: BinaryOp | UnaryOp | Number = self.peek_multiplicative_expression()

        while True:
            if self.is_token_kind(tk.TokenKind.ADD_OP):
                self.peek_token()  # peek the add op token

                sub_multiplicative_expression: BinaryOp | UnaryOp | Number = self.peek_multiplicative_expression()

                multiplicative_expression = BinaryOp(BinaryOpKind.Addition, multiplicative_expression, sub_multiplicative_expression)

            elif self.is_token_kind(tk.TokenKind.MIN_OP):
                self.peek_token()  # peek the min op token

                sub_multiplicative_expression: BinaryOp | UnaryOp | Number = self.peek_multiplicative_expression()

                multiplicative_expression = BinaryOp(BinaryOpKind.Subtraction, multiplicative_expression, sub_multiplicative_expression)
            else:
                return multiplicative_expression

    def peek_expression(self) -> BinaryOp | UnaryOp | Number:
        additive_expression: BinaryOp | UnaryOp | Number = self.peek_additive_expression()

        return additive_expression

    def parse(self):
        self.peek_token()  # peek the "-1" token

        self.AST = self.peek_expression()