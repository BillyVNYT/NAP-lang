from enum import Enum


class TokenType(Enum):
    NUMBER = "NUMBER"
    IDENTIFIER = "IDENTIFIER"

    PLUS = "+"
    MINUS = "-"
    STAR = "*"
    SLASH = "/"

    EQUAL = "="

    GREATER = ">"
    LESS = "<"
    GREATER_EQUAL = ">="
    LESS_EQUAL = "<="
    EQUAL_EQUAL = "=="
    NOT_EQUAL = "!="

    COMMA = ","
    COLON = ":"

    LEFT_PAREN = "("
    RIGHT_PAREN = ")"

    LEFT_BRACKET = "["
    RIGHT_BRACKET = "]"

    NEWLINE = "NEWLINE"
    INDENT = "INDENT"
    DEDENT = "DEDENT"

    EOF = "EOF"


class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value!r})"