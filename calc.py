from collections import OrderedDict
from math import sin, cos, tan, log10, sqrt, pi, e
import operator as op

operations = OrderedDict([
    ("+", op.iadd),
    ("-", op.isub),
    ("/", op.truediv),
    ("*", op.mul),
    ("^", op.pow),
    ('-u', op.neg),
    ('+u', op.pos),
    ("pi", pi),
    ("e", e),
    ("log", log10),
    ("sin", sin),
    ("cos", cos),
    ("tan", tan),
    ("sqrt", sqrt)
])

characters = operations.keys()


def separator(expr):
    tokens = []

    while expr:
        char, *expr = expr
        if char == "(":
            try:
                parenth, expr = separator(expr)
                tokens.append(parenth)
            except ValueError:
                raise Exception("missing parentheses!")
        elif char == ")":
            return tokens, expr

        elif char.isalpha():
            try:
                if tokens[-1] in characters:
                    tokens.append(char)
                else:
                    tokens[-1] += char
            except IndexError:
                tokens.append(char)

        elif char.isdigit() or char == ".":
            try:
                if tokens[-1] in characters:
                    tokens.append(char)
                else:
                    tokens[-1] += char
            except IndexError:
                tokens.append(char)
        elif char in characters:
            if (char == "+" or char == "-") and (len(tokens) == 0):
                char += 'u'
                tokens.append(char)
            else:
                tokens.append(char)
        elif char is " " or char is '"' or char is "'":
            pass
        else:
            raise Exception("Wrong character: " + char)
    print(tokens, "after parser")  # it's here for debugging purpose!
    return tokens


def calculate(tokens):
    for symbol, function in operations.items():
        try:
            pos = tokens.index(symbol)
            left = calculate(tokens[:pos])
            right = calculate(tokens[pos + 1:])

            if symbol in ["sin", "cos", "tan", "sqrt", "log", "-u", "+u"]:
                return function(right)
            elif symbol in ["pi", "e"]:
                return function
            else:
                return function(left, right)
        except ValueError:
            pass

    if len(tokens) == 1:
        try:
            return float(tokens[0])
        except TypeError:
            return calculate(tokens[0])


def calc(expr):
    return calculate(separator(expr))


while True:
    print(calc(input("Input: ")))
