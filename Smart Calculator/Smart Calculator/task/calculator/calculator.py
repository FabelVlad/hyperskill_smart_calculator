class Calculator:
    __slots__ = ('var_dict', 'math_sym_dict', 'priority_dict', 'command_dict')

    def __init__(self):
        self.var_dict = {}
        self.math_sym_dict = {'-': lambda x, y: x - y,
                              '+': lambda x, y: x + y,
                              '*': lambda x, y: x * y,
                              '/': lambda x, y: x / y,
                              '^': lambda x, y: x ^ y}
        self.command_dict = {'/exit': lambda: exit(),
                             '/help': lambda: '/-/'}
        self.priority_dict = {'-': 1, '+': 1, '*': 2, '/': 2, '^': 3, '(': 4, ')': 0}

    def _calc(self, x: int, y: int, symb: str) -> int:
        try:
            return self.math_sym_dict[symb](y, x)
        except ZeroDivisionError:
            pass

    def _check_for_invalid_double_symbols(self, expr: str):
        for s in list(self.math_sym_dict.keys())[2:]:
            for i in range(len(expr)):
                if s == expr[i] and s == expr[i - 1]:
                    print(s)
                    return False
        return True  # todo review method, can be static?? Yes

    def _get_variable(self, key: str) -> int:
        try:
            return self.var_dict[key]
        except KeyError:
            print('Unknown variable')

    def _make_elements_list(self, text: str):
        chars = [char if char.isnumeric() or char.isalpha() else f' {char} ' for char in text]
        return ''.join(chars).split()  # todo review

    def assign(self, key: str, value: int):
        self.var_dict[key] = value

    def command(self, key: str):
        try:
            self.command_dict[key]()
        except KeyError:
            print('Unknown command')

    def _convert_double_symbols(self, expr: str):
        chars = list(expr.replace(' ', ''))
        count = 1
        for i in range(len(chars) - 1):
            if chars[i] == chars[i + 1]:
                if chars[i] == list(self.math_sym_dict.keys())[1]:
                    chars[i] = ''
                elif chars[i] == list(self.math_sym_dict.keys())[0]:
                    count += 1
                    chars[i] = ''
            elif count > 1:
                if count % 2 == 0:
                    chars[i] = '+'
                else:
                    chars[i] = '-'
                count = 1
        return ''.join(chars)


    def validate_math_expression(self, expr: str) -> list:  # or None
        if self._check_for_invalid_double_symbols(expr) and expr.count('(') == expr.count(')'):
            # convert expr like ++ or ---- on equal
            expr = self._convert_double_symbols(expr)
            return calculator._make_elements_list(expr)
        else:
            print('Invalid expression')

    def view(self, key: str):
        print(self._get_variable(key))

    def calculate(self, expression: list):
        num_stack = []
        symbol_stack = []
        print(expression)
        for el in expression:
            if el == '(':
                symbol_stack.append(el)
            elif el == ')':
                while True:
                    if symbol_stack[-1] == '(':
                        symbol_stack.pop()
                        break
                    else:
                        num_stack.append(self._calc(num_stack.pop(), num_stack.pop(), symbol_stack.pop()))
            elif el in self.priority_dict:
                if symbol_stack == [] or symbol_stack[-1] == '(' or self.priority_dict[el] > self.priority_dict[symbol_stack[-1]]:
                    symbol_stack.append(el)
                elif self.priority_dict[symbol_stack[-1]] >= self.priority_dict[el]:
                    num_stack.append(self._calc(num_stack.pop(), num_stack.pop(), symbol_stack.pop()))
                    while True:
                        if not symbol_stack or symbol_stack[-1] == '(' or self.priority_dict[symbol_stack[-1]] < \
                                self.priority_dict[
                                    el]:
                            symbol_stack.append(el)
                            break
                        elif self.priority_dict[symbol_stack[-1]] >= self.priority_dict[el]:
                            num_stack.append(self._calc(num_stack.pop(), num_stack.pop(), symbol_stack.pop()))
                else:
                    num_stack.append(self._calc(num_stack.pop(), num_stack.pop(), el))
            else:
                num_stack.append(int(el))
        if num_stack:
            for el in num_stack:
                num_stack.append(self._calc(num_stack.pop(), num_stack.pop(), symbol_stack.pop()))
        print(num_stack[0])


if __name__ == '__main__':
    calculator = Calculator()
    while True:
        expression = input()
        if expression in calculator.command_dict:
            calculator.command(expression)
        elif '=' in expression:
            if len(expression.split()) < 4:
                expr_list = expression.replace(' ', '').split('=')
                if expr_list[0].isalpha():
                    if expr_list[1].isnumeric():
                        calculator.assign(expr_list[0], int(expr_list[1]))
                    elif expr_list[1] in calculator.var_dict:
                        calculator.assign(expr_list[0], calculator.var_dict[expr_list[1]])
                    else:
                        print('Invalid assignment')
                else:
                    print('Invalid identifier')
            else:
                print('Invalid assignment')  # todo review print, pay atantion on `f j = 8`
        elif expression.isalpha():
            calculator.view(expression)
        else:
            clear_expression = calculator.validate_math_expression(expression)
            calculator.calculate(clear_expression)
