# # write your code here
# import string
# letters = list(string.ascii_letters)
# command = '/exit'
# numbers = list(string.digits)
# symbols = ['-', '+']
# while True:
#     try:
#         text = input()
#         if ('/' not in text and text[0] in letters) or text[-1] in symbols:
#             print('Invalid expression')
#         elif '/' == text[0] and text != command:
#             print('Unknown command')
#         elif text == command:
#             print('Bye!')
#             exit()
#         else:
#             text_symbols = text.split()
#             flag = False
#             new_arr = []
#             if symbols[0] not in text and symbols[1] not in text:
#                 print('Invalid expression')
#             else:
#                 for i in range(len(text_symbols)):
#                     if text_symbols[i] == symbols[0]:
#                         flag = True
#                     elif flag:
#                         new_arr.append(int('-' + text_symbols[i]))
#                         flag = False
#                     elif text_symbols[i] == symbols[1]:
#                         pass
#                     else:
#                         new_arr.append(int(text_symbols[i]))
#             # print(new_arr)
#                 print(sum(new_arr))
#     except EOFError:
#         pass
#     except IndexError:
#         pass
#
#
#
#

import string

letters = list(string.ascii_letters)
commands = ['/exit', '/help']
degits = list(string.digits)
symbols = ['-', '+', '/', '*', '^']
my_dict = {'a': 4}
priority_dict = {'-': 1, '+': 1, '*': 2, '/': 2, '^': 3}


def check_identifier(expr):
    for char in expr:
        if char in degits:
            print('Invalid identifier')
            return True


def prepare_expression(expr):
    chars = list(expr)
    count = 0
    symb_stack = []
    for i in range(len(chars)):
        if chars[i] in degits:
            pass
        elif chars[i] == ' ':
            chars[i] = ''
        elif chars[i] == '(':
            count = count + 1
        elif chars[i] == ')':
            count = count - 1
        elif chars[i] in symbols:
            if chars[i] == chars[i + 1] and (chars[i] == '/' or chars[i] == '*' or chars[i] == '^'):
                print('Invalid expression')
                return False
            elif chars[i] == '*' or chars[i] == '/' or chars[i] == '^':
                pass
            elif chars[i] == chars[i + 1] and (chars[i] == '+' or chars[i] == '-'):
                symb_stack.append(chars[i])
                chars[i] = ''
            elif chars[i] != chars[i + 1] and symb_stack:
                symb_stack.append(chars[i])
                if chars[i] == '+':
                    symb_stack.clear()
                else:
                    if len(symb_stack) % 2 == 0:
                        chars[i] = '+'
                        symb_stack.clear()
                    else:
                        symb_stack.clear()
    if count != 0:
        print('Invalid expression')
        return False
    new_text = ''.join(chars)
    for el in new_text:
        if el in symbols or el == '(' or el == ')':
            new_text = new_text.replace(el, f' {el} ')
    return new_text.split()


def input_expression():
    expression = input()
    if '=' in expression:
        expression = expression.replace(' ', '').split('=')
        if 1 < len(expression) < 3:
            return expression, 'assiment'
        else:
            print('Invalid assignment')
            return False, False
    elif '/' in expression and expression[1] in letters:
        return expression, 'command'
    elif symbols[0] in expression or symbols[1] in expression or symbols[2] in expression or symbols[3] in expression or \
            symbols[4] in expression:
        expression = prepare_expression(expression)
        return expression, 'calculate'
    else:
        if expression == '':
            # print('\n')
            return False, False
        elif check_identifier(expression):
            return False, False
        return expression, 'view'


def do_command(command):
    if command in commands:
        if command == commands[0]:
            print('Bye!')
            exit()
    else:
        print('Unknown command')


def view(variable_name):
    if variable_name in my_dict:
        print(my_dict[variable_name])
    else:
        print('Unknown variable')


def calc(f: int, s: int, symb):
    if symb == '-':
        return s - f
    elif symb == '+':
        return s + f
    elif symb == '*':
        return s * f
    elif symb == '/':
        return s / f
    elif symb == '^':
        return s ^ f


def calculate(expression: list):
    num_stack = []
    symbol_stack = []
    for el in expression:
        if el == '(':
            symbol_stack.append(el)
        elif el == ')':
            while True:
                if symbol_stack[-1] == '(':
                    symbol_stack.pop()
                    break
                else:
                    num_stack.append(calc(num_stack.pop(), num_stack.pop(), symbol_stack.pop()))
        elif el in priority_dict:
            if symbol_stack == [] or symbol_stack[-1] == '(' or priority_dict[el] > priority_dict[symbol_stack[-1]]:
                symbol_stack.append(el)
            elif priority_dict[symbol_stack[-1]] >= priority_dict[el]:
                num_stack.append(calc(num_stack.pop(), num_stack.pop(), symbol_stack.pop()))
                while True:
                    if not symbol_stack or symbol_stack[-1] == '(' or priority_dict[symbol_stack[-1]] < \
                            priority_dict[el]:
                        symbol_stack.append(el)
                        break
                    elif priority_dict[symbol_stack[-1]] >= priority_dict[el]:
                        num_stack.append(calc(num_stack.pop(), num_stack.pop(), symbol_stack.pop()))
            else:
                num_stack.append(calc(num_stack.pop(), num_stack.pop(), el))
        elif el in letters:
            print('Invalid expression')
            break
        else:
            num_stack.append(int(el))

    if num_stack:
        for el in num_stack:
            num_stack.append(calc(num_stack.pop(), num_stack.pop(), symbol_stack.pop()))
    print(int(num_stack[0]))


def assignment(chars):
    left_expression = chars[0]
    right_expression = chars[1]
    if not check_identifier(left_expression):
        if right_expression in my_dict:
            my_dict[left_expression] = my_dict[right_expression]
        else:
            try:
                right_expression = int(right_expression)
                my_dict[left_expression] = right_expression
            except ValueError:
                print('Invalid assignment')


while True:
    variables, mode = input_expression()
    if variables:
        if mode == 'command':
            do_command(variables)
        elif mode == 'view':
            view(variables)
        elif mode == 'calculate':
            # variables = list(variables)
            for i in range(len(variables)):
                if variables[i] in my_dict:
                    variables[i] = my_dict[variables[i]]
            calculate(variables)
        elif mode == 'assiment':
            assignment(variables)
