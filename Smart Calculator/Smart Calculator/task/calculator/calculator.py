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

    def _check_for_double_symbols(self, expr: str):
        for s in list(self.math_sym_dict.keys())[2:]:
            if s in expr: return False
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

    def _replace_element(self, expr: str):
        expr_list = expr.replace(' ', '')

    def validate_math_expression(self, expr: str) -> list:
        if self._check_for_double_symbols(expr) and expr.count('(') == expr.count(')'):
            # replace expr like ++ or ---- on equal

            return calculator._make_elements_list(expr)
        else:
            print('Invalid expression')

    def view(self, key: str):
        print(self._get_variable(key))




if __name__ == '__main__':
    calculator = Calculator()
    while True:
        expression = input()
        if expression in calculator.math_sym_dict and len(expression) > 1:
            calculator.command(expression)
        elif '=' in expression:
            expr_list = expression.split()
            if len(expr_list) < 4:
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
            if calculator.validate_math_expression(expression):
                print(calculator.validate_math_expression(expression))  # calc will be receive list of elements of expr
