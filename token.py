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
    DOT = "."

    LEFT_PAREN = "("
    RIGHT_PAREN = ")"

    LEFT_BRACKET = "["
    RIGHT_BRACKET = "]"

    TRUE = "TRUE"
    FALSE = "FALSE"

    NEWLINE = "NEWLINE"
    INDENT = "INDENT"
    DEDENT = "DEDENT"

    AND = "and"
    OR = "or"
    NOT = "not"

    EOF = "EOF"

    STRING = "STRING"

    FLOAT = "FLOAT"

    BREAK = "break"
    CONTINUE = "continue"


class Token:
    def __init__(self, token_type, value):
        self.type = token_type
        self.value = value

    def __repr__(self):
        return f"Token({self.type}, {self.value!r})"