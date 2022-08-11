
def parse_expression_postfix():
    try:
        expr = input("Input binary postfix expression: (allowed operators: +, -, *, /,) ")
        A, B, op = expr.split()
    except ValueError:
        print("Invalid format, please input expression as: Operand1 Operand2 operator")
        return None

    try:
        float(A), float(B)
    except ValueError:
        print("One or more operands cannot be parsed as numeric; please check operands")
        return None

    try:
        valid_operators = {'+', '-', '*', '/'}
        if op not in valid_operators:
            raise ValueError("")

        exprval = eval(A + op + B)
        return exprval
    except ValueError:
        print("Invalid operator; legal operators are +, -, *, /")
        return None
    except ZeroDivisionError:
        print("Cannot divide by zero")
        return None
    except SyntaxError:
        print("Unexpected syntax error, sorry :(")
        return None

if __name__ == '__main__':
    value = None
    while value is None:
        value = parse_expression_postfix()
    print(value)


