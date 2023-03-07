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


class Operator:
    """operator node"""

    def __init__(self, type: OperatorType, left: 'Operator | Value', right: 'Operator | Value'):
        self.type = type
        self.left = left
        self.right = right

    def __str__(self):
        str_ = "("
        str_ += f"{self.left} "
        match self.type:
            case OperatorType.Addition: # presency
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

    def __init__(self, tokens: list[src.bee_token.Token]):
        self.tokens: list[src.bee_token.Token] = tokens
        self.start_node = Parser.parse_expression(self.tokens)

    @staticmethod
    def parse_literal(token: src.bee_token.Token) -> Value:
        match token.kind:
            case src.bee_token.TokenKind.Integer:
                return Value(int(token.string))
            case src.bee_token.TokenKind.Float:
                return Value(float(token.string))
            case _:
                raise RuntimeError("a literal token is needed")

    @staticmethod
    def parse_prefix(tokens: src.bee_token.Token) -> Value:
        match tokens[0].kind:
            case src.bee_token.TokenKind.Plus:
                match tokens[1].kind:
                    case src.bee_token.TokenKind.Integer:
                        return Value(int(tokens[0].string))
                    case src.bee_token.TokenKind.Float:
                        return Value(float(tokens[0].string))
                    case _:
                        raise RuntimeError("a literal token is needed")
            case src.bee_token.TokenKind.Minus:
                match tokens[1].kind:
                    case src.bee_token.TokenKind.Integer:
                        return Value(-int(tokens[0].string))
                    case src.bee_token.TokenKind.Float:
                        return Value(-float(tokens[0].string))
                    case _:
                        raise RuntimeError("a literal token is needed")
            case _:
                raise RuntimeError("a plus/minus token is needed")

    @staticmethod
    def parse_expression(tokens: list[src.bee_token.Token]) -> Operator | Value:
        if len(tokens) == 0:
            raise RuntimeError("no tokens entered")
        elif len(tokens) == 1:  # a literal
            return Parser.parse_literal(tokens[0])
        elif len(tokens) == 2:  # a prefix (+ | -) following a literal
            return Parser.parse_prefix([tokens[0], tokens[1]])

        """
        1. split the array into two by the first operator
        2. call the parse expression function of the right and on the left side
        3. construct the tree to the left and the right side of the operator
        """

        index = 0

        # check for prefix
        if tokens[index].kind in [src.bee_token.TokenKind.Plus, src.bee_token.TokenKind.Minus] and \
                tokens[index + 1].kind in [src.bee_token.TokenKind.Integer, src.bee_token.TokenKind.Float]:
            index = 2  # set the index to the following index of the prefix operator and the literal

        while index < len(tokens) and tokens[index].kind not in [src.bee_token.TokenKind.Plus, src.bee_token.TokenKind.Minus, src.bee_token.TokenKind.Asterisk, src.bee_token.TokenKind.ForwardSlash]:
            index += 1

        left_tree = Parser.parse_expression(tokens[:index])
        right_tree = Parser.parse_expression(tokens[index + 1:])

        match tokens[index].kind:
            case src.bee_token.TokenKind.Plus:
                return Operator(OperatorType.Addition, left_tree, right_tree)
            case src.bee_token.TokenKind.Minus:
                return Operator(OperatorType.Subtraction, left_tree, right_tree)
            case src.bee_token.TokenKind.Asterisk:
                return Operator(OperatorType.Multiplication, left_tree, right_tree)
            case src.bee_token.TokenKind.ForwardSlash:
                return Operator(OperatorType.Division, left_tree, right_tree)
