import ast
import math
import operator as op

# Allowed binary operators
ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
}

# Allowed names & functions
ALLOWED_NAMES = {
    "sqrt": math.sqrt,
    "log": math.log10,
    "ln": math.log,
    "pow": math.pow,
    "pi": math.pi,
    "e": math.e,
}

def safe_eval(expr: str):
    def _eval(node):

        # Numbers (Python 3.8+)
        if isinstance(node, ast.Constant):
            if isinstance(node.value, (int, float)):
                return node.value
            raise ValueError("Invalid constant")

        # Numbers (Python <3.8)
        if isinstance(node, ast.Num):
            return node.n

        # Binary operations
        if isinstance(node, ast.BinOp):
            op_type = type(node.op)
            if op_type not in ALLOWED_OPERATORS:
                raise ValueError("Operator not allowed")
            return ALLOWED_OPERATORS[op_type](
                _eval(node.left),
                _eval(node.right)
            )

        # Unary operations (+ / -)
        if isinstance(node, ast.UnaryOp):
            if isinstance(node.op, ast.UAdd):
                return _eval(node.operand)
            if isinstance(node.op, ast.USub):
                return -_eval(node.operand)
            raise ValueError("Unary operator not allowed")

        # Function calls
        if isinstance(node, ast.Call):
            if not isinstance(node.func, ast.Name):
                raise ValueError("Invalid function call")

            func_name = node.func.id
            if func_name not in ALLOWED_NAMES:
                raise ValueError("Function not allowed")

            args = [_eval(arg) for arg in node.args]
            return ALLOWED_NAMES[func_name](*args)

        # Constants like pi, e
        if isinstance(node, ast.Name):
            if node.id in ALLOWED_NAMES:
                return ALLOWED_NAMES[node.id]
            raise ValueError("Name not allowed")

        raise ValueError("Unsafe expression")

    tree = ast.parse(expr, mode="eval").body
    return _eval(tree)
