from token import TokenType, Token


class Lexer:
    def __init__(self, source):
        self.source = source
        self.position = 0
        self.indent_stack = [0]

    def current(self):
        if self.position >= len(self.source):
            return "\0"

        return self.source[self.position]

    def advance(self):
        self.position += 1

    def read_number(self):
        value = ""

        while self.current().isdigit():
            value += self.current()
            self.advance()

        return Token(TokenType.NUMBER, value)

    def read_identifier(self):
        value = ""

        while self.current().isalnum() or self.current() == "_":
            value += self.current()
            self.advance()

        return Token(TokenType.IDENTIFIER, value)

    def tokenize(self):
        tokens = []
        at_line_start = True

        while self.current() != "\0":
            if at_line_start:
                spaces = 0

                while self.current() == " ":
                    spaces += 1
                    self.advance()

                if self.current() == "\n":
                    self.advance()
                    tokens.append(Token(TokenType.NEWLINE, "\\n"))
                    continue

                if spaces > self.indent_stack[-1]:
                    self.indent_stack.append(spaces)
                    tokens.append(Token(TokenType.INDENT, ""))

                elif spaces < self.indent_stack[-1]:
                    while spaces < self.indent_stack[-1]:
                        self.indent_stack.pop()
                        tokens.append(Token(TokenType.DEDENT, ""))

                at_line_start = False
            if self.current() == "\n":
                tokens.append(Token(TokenType.NEWLINE, "\\n"))
                self.advance()
                at_line_start = True
                continue

            if self.current().isspace():
                self.advance()
                continue

            if self.current().isdigit():
                tokens.append(self.read_number())
                continue

            if self.current().isalpha() or self.current() == "_":
                tokens.append(self.read_identifier())
                continue

            c = self.current()

            if c == "+":
                tokens.append(Token(TokenType.PLUS, c))
                self.advance()
                continue

            if c == "-":
                tokens.append(Token(TokenType.MINUS, c))
                self.advance()
                continue

            if c == "*":
                tokens.append(Token(TokenType.STAR, c))
                self.advance()
                continue

            if c == "/":
                tokens.append(Token(TokenType.SLASH, c))
                self.advance()
                continue

            if c == "=":
                self.advance()

                if self.current() == "=":
                    self.advance()
                    tokens.append(Token(TokenType.EQUAL_EQUAL, "=="))
                else:
                    tokens.append(Token(TokenType.EQUAL, "="))

                continue

            if c == "(":
                tokens.append(Token(TokenType.LEFT_PAREN, c))
                self.advance()
                continue

            if c == ")":
                tokens.append(Token(TokenType.RIGHT_PAREN, c))
                self.advance()
                continue

            if c == "!":
                self.advance()

                if self.current() == "=":
                    self.advance()
                    tokens.append(Token(TokenType.NOT_EQUAL, "!="))
                    continue

                raise SyntaxError("Expected '=' after '!'")

            if c == ">":
                self.advance()

                if self.current() == "=":
                    self.advance()
                    tokens.append(Token(TokenType.GREATER_EQUAL, ">="))
                else:
                    tokens.append(Token(TokenType.GREATER, ">"))

                continue

            if c == "<":
                self.advance()

                if self.current() == "=":
                    self.advance()
                    tokens.append(Token(TokenType.LESS_EQUAL, "<="))
                else:
                    tokens.append(Token(TokenType.LESS, "<"))

                continue

            if c == ":":
                tokens.append(Token(TokenType.COLON, c))
                self.advance()
                continue

            if c == ",":
                tokens.append(Token(TokenType.COMMA, c))
                self.advance()
                continue

            if c == "[":
                tokens.append(Token(TokenType.LEFT_BRACKET, c))
                self.advance()
                continue

            if c == "]":
                tokens.append(Token(TokenType.RIGHT_BRACKET, c))
                self.advance()
                continue

            raise SyntaxError(f"Unknown character: {c}")

        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            tokens.append(Token(TokenType.DEDENT, ""))

        tokens.append(Token(TokenType.EOF, ""))

        return tokens