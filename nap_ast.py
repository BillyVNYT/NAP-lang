from environment import Environment

class NumberExpr:
    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        return self.value

class VariableExpr:
    def __init__(self, name):
        self.name = name

    def evaluate(self, env):
        return env.get(self.name)

class AssignmentExpr:
    def __init__(self, name, value):
        self.name = name
        self.value = value

    def evaluate(self, env):
        value = self.value.evaluate(env)
        env.set(self.name, value)
        return value

class IfStmt:
    def __init__(self, condition, body, else_body=None):
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def evaluate(self, env):
        if self.condition.evaluate(env):
            result = None

            for statement in self.body:
                result = statement.evaluate(env)

            return result

        if self.else_body is not None:
            result = None

            for statement in self.else_body:
                result = statement.evaluate(env)

            return result

        return None

class BinaryExpr:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right

    def evaluate(self, env):
        left = self.left.evaluate(env)
        right = self.right.evaluate(env)

        if self.operator == "+":
            return left + right

        if self.operator == "-":
            return left - right

        if self.operator == "*":
            return left * right

        if self.operator == "/":
            return left / right

        if self.operator == ">":
            return left > right

        if self.operator == "<":
            return left < right

        if self.operator == ">=":
            return left >= right

        if self.operator == "<=":
            return left <= right

        if self.operator == "==":
            return left == right

        if self.operator == "!=":
            return left != right

        if self.operator == "and":
            return bool(left) and bool(right)

        if self.operator == "or":
            return bool(left) or bool(right)

        raise RuntimeError(f"Unknown operator: {self.operator}")

class WhileStmt:
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body

    def evaluate(self, env):
        result = None

        while self.condition.evaluate(env):
            for statement in self.body:
                result = statement.evaluate(env)

        return result

class ReturnSignal(Exception):
    def __init__(self, value):
        self.value = value

class ReturnStmt:
    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        value = self.value.evaluate(env)
        raise ReturnSignal(value)

class FunctionStmt:
    def __init__(self, name, parameters, body):
        self.name = name
        self.parameters = parameters
        self.body = body

    def evaluate(self, env):
        env.set(self.name, self)
        return None

    def call(self, arguments, env):
        if len(arguments) != len(self.parameters):
            raise RuntimeError(
                f"Expected {len(self.parameters)} arguments, "
                f"got {len(arguments)}"
            )

        local_env = Environment()

        for name, value in zip(self.parameters, arguments):
            local_env.set(name, value)

        try:
            for statement in self.body:
                statement.evaluate(local_env)

        except ReturnSignal as signal:
            return signal.value

        return None

class CallExpr:
    def __init__(self, function, arguments):
        self.function = function
        self.arguments = arguments

    def evaluate(self, env):
        function = self.function.evaluate(env)

        arguments = [
            argument.evaluate(env)
            for argument in self.arguments
        ]

        return function.call(arguments, env)

class BuiltinFunction:
    def __init__(self, function):
        self.function = function

    def call(self, arguments, env):
        return self.function(arguments)

class ListExpr:
    def __init__(self, elements):
        self.elements = elements

    def evaluate(self, env):
        return [
            element.evaluate(env)
            for element in self.elements
        ]

class ListIndexExpr:
    def __init__(self, list_expr, index_expr):
        self.list_expr = list_expr
        self.index_expr = index_expr

    def evaluate(self, env):
        lst = self.list_expr.evaluate(env)
        index = self.index_expr.evaluate(env)

        if not isinstance(index, int):
            raise RuntimeError("List index must be an integer")

        try:
            return lst[index]
        except IndexError:
            raise RuntimeError("List index out of range")

class BooleanExpr:
    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        return self.value

class ForStmt:
    def __init__(self, variable, iterable, body):
        self.variable = variable
        self.iterable = iterable
        self.body = body

    def evaluate(self, env):
        values = self.iterable.evaluate(env)

        if not isinstance(values, list):
            raise RuntimeError("Object is not iterable")

        result = None

        for value in values:
            env.set(self.variable, value)

            for statement in self.body:
                result = statement.evaluate(env)

        return 

class UnaryExpr:
    def __init__(self, operator, operand):
        self.operator = operator
        self.operand = operand

    def evaluate(self, env):
        value = self.operand.evaluate(env)

        if self.operator == "not":
            return not bool(value)

        raise RuntimeError(
            f"Unknown unary operator: {self.operator}"
        )

class StringExpr:
    def __init__(self, value):
        self.value = value

    def evaluate(self, env):
        return self.value