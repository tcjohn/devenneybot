import re

import dice


dice_notation_pattern = re.compile('^(\d+(d\d+)?([\+\-\/\*](?!$))?){1,}$')
single_dice_notation_pattern = re.compile('^\d+d\d+$')


def is_valid_dice_notation(string: str) -> bool:
    return dice_notation_pattern.match(string)


def is_valid_single_dice_notation(string: str) -> bool:
    return single_dice_notation_pattern.match(string)


def is_number(string: str) -> bool:
    try:
        int(string)
        return True
    except ValueError:
        return False


def peek(stack: list) -> list:
    return stack[-1] if stack else None


def apply_operator(operators: list, values: list, rolls: list):
    operator = operators.pop()
    right = values.pop()
    left = values.pop()
    if operator == 'd':
        r = dice.roll("{}{}{}".format(left, operator, right))
        rolls.append(r)
        value = 0
        for roll in r:
            value += int(roll)
        values.append(value)
    else:
        values.append(eval("{0}{1}{2}".format(left, operator, right)))


def greater_precedence(op1: str, op2: str) -> bool:
    precedences = {'+' : 0, '-' : 0, '*' : 1, '/' : 1, 'd': 2}
    return precedences[op1] > precedences[op2]


def handicap(type: str, expression: str) -> (int, list):
    rolls = []
    rolls.append(dice.roll(expression))
    rolls.append(dice.roll(expression))

    total = -1
    if type == 'advantage':
        total = max(rolls)
    elif type == 'disadvantage':
        total = min(rolls)
    return int(total), rolls


def evaluate(expression: str) -> (int, list):
    tokens = re.findall("[d+/*()-]|\d+", expression)

    rolls = []
    values = []
    operators = []
    for token in tokens:
        if is_number(token):
            values.append(int(token))
        elif token == '(':
            operators.append(token)
        elif token == ')':
            top = peek(operators)
            while top is not None and top != '(':
                apply_operator(operators, values, rolls)
                top = peek(operators)
            operators.pop() # Discard the '('
        else:
            # Operator
            top = peek(operators)
            while top is not None and top not in "()" and greater_precedence(top, token):
                apply_operator(operators, values, rolls)
                top = peek(operators)
            operators.append(token)
    while peek(operators) is not None:
        apply_operator(operators, values, rolls)

    return sum(values), rolls