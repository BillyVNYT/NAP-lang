import math
import builtins


def register_builtins(env, BuiltinFunction):
    env.set(
        "print",
        BuiltinFunction(lambda args: print(*args))
    )

    env.set(
        "len",
        BuiltinFunction(lambda args: len(args[0]))
    )

    env.set(
        "sqrt",
        BuiltinFunction(lambda args: math.sqrt(args[0]))
    )

    env.set(
        "pow",
        BuiltinFunction(lambda args: args[0] ** args[1])
    )

    env.set(
        "abs",
        BuiltinFunction(lambda args: builtins.abs(args[0]))
    )

    env.set(
        "sin",
        BuiltinFunction(lambda args: math.sin(args[0]))
    )

    env.set(
        "cos",
        BuiltinFunction(lambda args: math.cos(args[0]))
    )

    env.set(
        "exp",
        BuiltinFunction(lambda args: math.exp(args[0]))
    )

    env.set(
        "log",
        BuiltinFunction(lambda args: math.log(args[0]))
    )

    env.set(
        "range",
        BuiltinFunction(billy_range)
    )

def billy_range(args):
    if len(args) == 1:
        return list(range(args[0]))

    if len(args) == 2:
        return list(range(args[0], args[1]))

    if len(args) == 3:
        return list(range(args[0], args[1], args[2]))

    raise RuntimeError("range() expects 1, 2, or 3 arguments")