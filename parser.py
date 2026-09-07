from token import TokenType

from nap_ast import (
    NumberExpr,
    BooleanExpr,
    StringExpr,
    BinaryExpr,
    VariableExpr,
    AssignmentExpr,
    IfStmt,
    WhileStmt,
    ReturnStmt,
    FunctionStmt,
    CallExpr,
    ListExpr,
    ListIndexExpr,
    ForStmt,
    UnaryExpr
)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0

    def current(self):
        return self.tokens[self.position]

    def advance(self):
        self.position += 1

    def parse_factor(self):
        token = self.current()

        if token.type == TokenType.NOT:
            self.advance()
            operand = self.parse_factor()
            return UnaryExpr("not", operand)

        if token.type == TokenType.NUMBER:
            self.advance()
            return NumberExpr(int(token.value))

        if token.type == TokenType.TRUE:
            self.advance()
            return BooleanExpr(True)

        if token.type == TokenType.FALSE:
            self.advance()
            return BooleanExpr(False)

        if token.type == TokenType.STRING:
            self.advance()
            return StringExpr(token.value)

        if token.type == TokenType.LEFT_BRACKET:
            self.advance()

            elements = []

            if self.current().type != TokenType.RIGHT_BRACKET:
                while True:
                    elements.append(self.parse_or())

                    if self.current().type == TokenType.RIGHT_BRACKET:
                        break

                    if self.current().type != TokenType.COMMA:
                        raise SyntaxError("Expected ','")

                    self.advance()

            self.advance()

            return ListExpr(elements)

        if token.type == TokenType.IDENTIFIER:
            self.advance()

            expr = VariableExpr(token.value)

            if self.current().type == TokenType.LEFT_PAREN:
                self.advance()

                arguments = []

                if self.current().type != TokenType.RIGHT_PAREN:
                    while True:
                        arguments.append(self.parse_or())

                        if self.current().type == TokenType.RIGHT_PAREN:
                            break

                        if self.current().type != TokenType.COMMA:
                            raise SyntaxError("Expected ','")

                        self.advance()

                self.advance()

                expr = CallExpr(expr, arguments)

            while self.current().type == TokenType.LEFT_BRACKET:
                self.advance()

                index = self.parse_expression()

                if self.current().type != TokenType.RIGHT_BRACKET:
                    raise SyntaxError("Expected ']'")

                self.advance()

                expr = ListIndexExpr(expr, index)

            return expr

        raise SyntaxError(f"Unexpected token: {token}")

    def parse_term(self):
        left = self.parse_factor()

        while (
            self.current().type == TokenType.STAR
            or self.current().type == TokenType.SLASH
        ):
            operator = self.current().value
            self.advance()

            right = self.parse_factor()

            left = BinaryExpr(left, operator, right)

        return left

    def parse_expression(self):
        left = self.parse_term()

        while (
            self.current().type == TokenType.PLUS
            or self.current().type == TokenType.MINUS
        ):
            operator = self.current().value
            self.advance()

            right = self.parse_term()

            left = BinaryExpr(left, operator, right)

        return left

    def parse_assignment(self):
        if (
            self.current().type == TokenType.IDENTIFIER
            and self.tokens[self.position + 1].type == TokenType.EQUAL
        ):
            name = self.current().value

            self.advance()
            self.advance()

            value = self.parse_or()

            return AssignmentExpr(name, value)

        return self.parse_or()

    def parse_statement(self):
        if (
            self.current().type == TokenType.IDENTIFIER
            and self.current().value == "if"
        ):
            return self.parse_if()

        if (
            self.current().type == TokenType.IDENTIFIER
            and self.current().value == "while"
        ):
            return self.parse_while()

        if (
            self.current().type == TokenType.IDENTIFIER
            and self.current().value == "return"
        ):
            self.advance()

            value = self.parse_comparison()

            return ReturnStmt(value)

        if (
            self.current().type == TokenType.IDENTIFIER
            and self.current().value == "function"
        ):
            return self.parse_function()

        if (
            self.current().type == TokenType.IDENTIFIER
            and self.current().value == "for"
        ):
            return self.parse_for()

        return self.parse_assignment()

    def parse_program(self):
        statements = []

        while self.current().type != TokenType.EOF:

            if self.current().type == TokenType.NEWLINE:
                self.advance()
                continue

            statements.append(self.parse_statement())

            if self.current().type == TokenType.NEWLINE:
                self.advance()

        return statements

    def parse_comparison(self):
        left = self.parse_expression()

        while self.current().type in (
            TokenType.GREATER,
            TokenType.LESS,
            TokenType.GREATER_EQUAL,
            TokenType.LESS_EQUAL,
            TokenType.EQUAL_EQUAL,
            TokenType.NOT_EQUAL,
        ):
            operator = self.current().value
            self.advance()

            right = self.parse_expression()

            left = BinaryExpr(left, operator, right)

        return left

    def parse_if(self):
        self.advance()

        condition = self.parse_comparison()

        if self.current().type != TokenType.COLON:
            raise SyntaxError("Expected ':' after if condition")

        self.advance()

        if self.current().type != TokenType.NEWLINE:
            raise SyntaxError("Expected newline after ':'")

        self.advance()

        if self.current().type != TokenType.INDENT:
            raise SyntaxError("Expected indentation")

        self.advance()

        body = []

        while self.current().type != TokenType.DEDENT:
            if self.current().type == TokenType.EOF:
                raise SyntaxError("Expected DEDENT")

            if self.current().type == TokenType.NEWLINE:
                self.advance()
                continue

            body.append(self.parse_statement())

            if self.current().type == TokenType.NEWLINE:
                self.advance()

        self.advance()

        # Kiểm tra xem phía sau có else không
        else_body = None

        if (
            self.current().type == TokenType.IDENTIFIER
            and self.current().value == "else"
        ):
            self.advance()

            if self.current().type != TokenType.COLON:
                raise SyntaxError("Expected ':' after else")

            self.advance()

            if self.current().type != TokenType.NEWLINE:
                raise SyntaxError("Expected newline after ':'")

            self.advance()

            if self.current().type != TokenType.INDENT:
                raise SyntaxError("Expected indentation")

            self.advance()

            else_body = []

            while self.current().type != TokenType.DEDENT:
                if self.current().type == TokenType.EOF:
                    raise SyntaxError("Expected DEDENT")

                if self.current().type == TokenType.NEWLINE:
                    self.advance()
                    continue

                else_body.append(self.parse_statement())

                if self.current().type == TokenType.NEWLINE:
                    self.advance()

            self.advance()

        return IfStmt(condition, body, else_body)

    def parse_while(self):
        self.advance()

        condition = self.parse_comparison()

        if self.current().type != TokenType.COLON:
            raise SyntaxError("Expected ':' after while condition")

        self.advance()

        if self.current().type != TokenType.NEWLINE:
            raise SyntaxError("Expected newline after ':'")

        self.advance()

        if self.current().type != TokenType.INDENT:
            raise SyntaxError("Expected indentation")

        self.advance()

        body = []

        while self.current().type != TokenType.DEDENT:
            if self.current().type == TokenType.EOF:
                raise SyntaxError("Expected DEDENT")

            if self.current().type == TokenType.NEWLINE:
                self.advance()
                continue

            body.append(self.parse_statement())

            if self.current().type == TokenType.NEWLINE:
                self.advance()

        self.advance()

        return WhileStmt(condition, body)

    def parse_function(self):
        # bỏ qua "function"
        self.advance()

        # tên function
        if self.current().type != TokenType.IDENTIFIER:
            raise SyntaxError("Expected function name")

        name = self.current().value
        self.advance()

        # (
        if self.current().type != TokenType.LEFT_PAREN:
            raise SyntaxError("Expected '('")

        self.advance()

        parameters = []

        # đọc parameters
        if self.current().type != TokenType.RIGHT_PAREN:
            while True:
                if self.current().type != TokenType.IDENTIFIER:
                    raise SyntaxError("Expected parameter name")

                parameters.append(self.current().value)
                self.advance()

                if self.current().type == TokenType.RIGHT_PAREN:
                    break

                if self.current().value != ",":
                    raise SyntaxError("Expected ','")

                self.advance()

        # )
        self.advance()

        # :
        if self.current().type != TokenType.COLON:
            raise SyntaxError("Expected ':'")

        self.advance()

        # newline
        if self.current().type != TokenType.NEWLINE:
            raise SyntaxError("Expected newline")

        self.advance()

        # indent
        if self.current().type != TokenType.INDENT:
            raise SyntaxError("Expected indentation")

        self.advance()

        body = []

        while self.current().type != TokenType.DEDENT:
            if self.current().type == TokenType.EOF:
                raise SyntaxError("Expected DEDENT")

            if self.current().type == TokenType.NEWLINE:
                self.advance()
                continue

            body.append(self.parse_statement())

            if self.current().type == TokenType.NEWLINE:
                self.advance()

        self.advance()

        return FunctionStmt(name, parameters, body)

    def parse_for(self):
        # bỏ qua "for"
        self.advance()

        # tên biến
        if self.current().type != TokenType.IDENTIFIER:
            raise SyntaxError("Expected variable after 'for'")

        variable = self.current().value
        self.advance()

        # phải có "in"
        if (
            self.current().type != TokenType.IDENTIFIER
            or self.current().value != "in"
        ):
            raise SyntaxError("Expected 'in'")

        self.advance()

        # thứ sẽ lặp
        iterable = self.parse_expression()

        # :
        if self.current().type != TokenType.COLON:
            raise SyntaxError("Expected ':' after for")

        self.advance()

        # newline
        if self.current().type != TokenType.NEWLINE:
            raise SyntaxError("Expected newline after ':'")

        self.advance()

        # indent
        if self.current().type != TokenType.INDENT:
            raise SyntaxError("Expected indentation")

        self.advance()

        body = []

        while self.current().type != TokenType.DEDENT:
            if self.current().type == TokenType.EOF:
                raise SyntaxError("Expected DEDENT")

            if self.current().type == TokenType.NEWLINE:
                self.advance()
                continue

            body.append(self.parse_statement())

            if self.current().type == TokenType.NEWLINE:
                self.advance()

        self.advance()

        return ForStmt(variable, iterable, body)

    def parse_or(self):
        left = self.parse_and()

        while self.current().type == TokenType.OR:
            self.advance()

            right = self.parse_and()

            left = BinaryExpr(left, "or", right)

        return left

    def parse_and(self):
        left = self.parse_comparison()

        while self.current().type == TokenType.AND:
            self.advance()

            right = self.parse_comparison()

            left = BinaryExpr(left, "and", right)

        return left

    def parse_or(self):
        left = self.parse_and()

        while self.current().type == TokenType.OR:
            self.advance()

            right = self.parse_and()

            left = BinaryExpr(left, "or", right)

        return left