import enum


class TokenKind(enum.IntEnum):
    Pluss = enum.auto()  # +
    Minus = enum.auto()  # -
    Asterisk = enum.auto()  # *
    ForwardSlash = enum.auto()  # /
    Integer = enum.auto()
    Float = enum.auto()


class Token:
    def __init__(self, kind: TokenKind, string: str) -> None:
        self.kind: TokenKind = kind
        self.string: str = string
