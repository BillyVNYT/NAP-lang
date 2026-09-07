from lexer import Lexer
from parser import Parser
from environment import Environment
from nap_ast import BuiltinFunction
import sys
from runtime.builtins import register_builtins

if len(sys.argv) < 2:
    print("Usage: billy <test.nap>")
    sys.exit(1)


filename = sys.argv[1]

with open(filename, "r", encoding="utf-8") as f:
    code = f.read()


lexer = Lexer(code)
tokens = lexer.tokenize()

parser = Parser(tokens)
program = parser.parse_program()

env = Environment()

env.set(
    "print",
    BuiltinFunction(
        lambda args: print(*args)
    )
)

env.set(
    "len",
    BuiltinFunction(
        lambda args: len(args[0])
    )
)

register_builtins(env, BuiltinFunction)

for statement in program:
    statement.evaluate(env)