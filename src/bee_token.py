import enum


class TokenKind(enum.IntEnum):
    Plus = enum.auto()  # +
    Minus = enum.auto()  # -
    Asterisk = enum.auto()  # *
    ForwardSlash = enum.auto()  # /
    Integer = enum.auto()
    Float = enum.auto()
    OpenParenthesis = enum.auto()  # (
    ClosingParenthesis = enum.auto()  # )
    Comma = enum.auto()  # ,
    Identifier = enum.auto()  # ,
    END = enum.auto()  # end token



class Token:
    def __init__(self, kind: TokenKind, string: str) -> None:
        self.kind: TokenKind = kind
        self.string: str = string
