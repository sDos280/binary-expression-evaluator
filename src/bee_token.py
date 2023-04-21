import enum


class TokenKind(enum.Enum):
    ADD_OP = enum.auto()  # +
    MIN_OP = enum.auto()  # -
    MUL_OP = enum.auto()  # *
    DIV_OP = enum.auto()  # /

    OpenParenthesis = enum.auto()  # (
    ClosingParenthesis = enum.auto()  # )
    Comma = enum.auto()  # ,

    Integer = enum.auto()
    Float = enum.auto()
    Identifier = enum.auto()
    END = enum.auto()  # end tokens string token


class Token:
    def __init__(self, kind: TokenKind, string: str) -> None:
        self.kind: TokenKind = kind
        self.string: str = string
