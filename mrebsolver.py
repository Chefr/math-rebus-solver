import re


class CodedDigit:
    """Represents the coded digit"""

    def __init__(self):
        self.digit = None
        self.not_null = False  # True if digit cannot be 0, False otherwise

    def __repr__(self):
        return str(self.digit)


class CodedDigitFactory:
    """Factory of Coded Digits"""

    def __init__(self):
        self.cache = {}  # e.g. {'a': CodedDigit()}

    def get(self, symbol):
        """
        Returns the Coded Digit corresponding to the specified symbol
        :param symbol: Code symbol, e.g. 'A'
        :return: Coded Digit
        """
        if symbol.isdigit():  # Simple digit
            return symbol
        if symbol in self.cache:
            return self.cache.get(symbol)
        code_digit = CodedDigit()
        self.cache[symbol] = code_digit
        return code_digit


class CodedNumber:
    """Represents the coded number as the sequence of Coded Digits"""

    def __init__(self, coded_digits, coded_digit_factory):
        """
        :param coded_digits: Str represents sequence of Coded Digits e.g. 'SEND'
        :param coded_digit_factory: Coded Digit Factory
        """
        self._coded_digits = list(map(lambda symbol:
                                  coded_digit_factory.get(symbol),
                                  coded_digits))
        self.is_positive = True
        coded_digit = self._coded_digits[0]
        if isinstance(coded_digit, CodedDigit):
            coded_digit.not_null = True  # First digit of number cannot be 0

    def __int__(self):
        str_digit = ''
        for coded_digit in self._coded_digits:
            str_digit += str(coded_digit)
        return int(str_digit) if self.is_positive else -int(str_digit)

    def __repr__(self):
        return ''.join(map(lambda digit: str(digit), self._coded_digits))


class CodedExpression:
    """Represents the coded expression. Calculation algorithm is taken from
    R.Lafore. "Data Structures and Algorithms in Java" and needs optimization"""

    def __init__(self, coded_expression, factory):
        """
        :param coded_expression: Str sequence of Coded Numbers and operators
        e.g. SEND + MORE
        :param factory: Coded Digit Factory
        """
        items = re.split('(\W)', coded_expression)
        items = list(filter(lambda s: len(s) > 0, items))
        self._items = list(map(lambda item: CodedNumber(item, factory) if
                           item[0].isalnum() else item,
                           items))
        self._infix_items = []
        self._parse()
        self._stack = []

    def __int__(self):
        if len(self._items) == 1:
            return int(self._items[0])
        stack = self._stack
        for item in self._infix_items:
            if isinstance(item, CodedNumber):
                stack.append(int(item))
            else:
                num2 = stack.pop()
                num1 = stack.pop()
                if item == '+':
                    result = num1 + num2
                elif item == '-':
                    result = num1 - num2
                elif item == '*':
                    result = num1 * num2
                else:
                    result = int(num1 / num2)
                stack.append(result)
        return stack.pop()

    def __repr__(self):
        str_expr = ''
        for i in range(len(self._items)):
            if i != 0:
                str_expr += ' '
            str_expr += str(self._items[i])
        return str_expr

    def _parse(self):
        if len(self._items) == 1:
            self._infix_items = self._items
            return
        stack = []
        for idx, item in enumerate(self._items):
            if idx == 0 and not isinstance(item, CodedNumber):
                if item == '-' and isinstance(self._items[1], CodedNumber):
                    self._items[1].is_positive = False
                    continue
                if item != '(':
                    raise IOError('Incorrect equation.'
                                  'Incorrect or redundant operator ' +
                                  item + ' at the beginning of an expression')
            if not isinstance(item, CodedNumber):
                if item == '+' or item == '-':
                    self._parse_operator(item, 1, stack)
                elif item == '*' or item == '/':
                    self._parse_operator(item, 2, stack)
                elif item == '(':
                    stack.append(item)
                elif item == ')':
                    self._parse_brackets(stack)
                else:
                    raise IOError('Incorrect equation. Unknown operator "' + item + '".')
            else:
                self._infix_items.append(item)
        while len(stack) > 0:
            item = stack.pop()
            if item == '(':
                raise IOError('Incorrect equation. incorrect brackets placement.')
            self._infix_items.append(item)

    def _parse_operator(self, operator, priority, stack):
        while len(stack) > 0:
            prev_item = stack.pop()
            if prev_item == '(':
                stack.append(prev_item)
                break
            else:
                if prev_item == '+' or prev_item == '-':
                    prev_item_priority = 1
                else:
                    prev_item_priority = 2
                if prev_item_priority < priority:
                    stack.append(prev_item)
                    break
                else:
                    self._infix_items.append(prev_item)
        stack.append(operator)

    def _parse_brackets(self, stack):
        while len(stack) > 0:
            item = stack.pop()
            if item == '(':
                break
            self._infix_items.append(item)
        else:
            raise IOError('Incorrect equation. incorrect brackets placement.')


class MathRebusSolver:
    """Generates solutions of the mathematical rebus"""

    def __init__(self, coded_equation):
        """
        :param coded_equation: Str representation of the equation, where digits
        replaced by letters. Valid operators: + - * /. Brackets () are allowed.
        E.g. SEND + MORE = MONEY
        """
        self._parts = re.sub('\s+', '', coded_equation).split('=')
        if len(self._parts) == 1:
            raise IOError('Incorrect equation. No sign equals (=)')
        self._factory = CodedDigitFactory()
        self._parts = list(map(lambda part:
                           CodedExpression(part, self._factory),
                           self._parts))
        self._coded_digits = list(self._factory.cache.values())
        self._coded_digits_len = len(self._coded_digits)
        self._free = [True] * 10  # Number of different digits
        self._layer = 0

    def get_solution_generator(self):
        return self._generate_solution()

    def _generate_solution(self):
        """Returns the solution generator"""
        for i in range(10):
            if not self._free[i]:
                continue
            coded_digit = self._coded_digits[self._layer]
            if coded_digit.not_null and i == 0:
                continue
            coded_digit.digit = i
            if self._layer == self._coded_digits_len - 1:
                try:
                    if int(self._parts[0]) == int(self._parts[1]):
                        yield MathRebusSolution(str(self),
                                                {item[0]: item[1].digit
                                                 for item in
                                                 self._factory.cache.items()})
                except ZeroDivisionError:
                    continue
                except IndexError:
                    raise IOError('Incorrect equation.')
            else:
                self._free[i] = False
                self._layer += 1
                yield from self._generate_solution()
                self._free[i] = True
                self._layer -= 1

    def __repr__(self):
        return ' = '.join(map(lambda part: str(part), self._parts))


class MathRebusSolution:
    """Represent the solution of the mathematical rebus"""

    def __init__(self, decoded_equation, decoded_digits):
        """
        :param decoded_equation: Str representation of the decoded equation
        :param decoded_digits: Dict, represent decoded digits,
        e.g. {'A' : 1, 'B' : 2 etc.}
        """
        self.decoded_equation = decoded_equation
        self.decoded_digits = decoded_digits

    def __repr__(self):
        return self.decoded_equation + ' ' + str(self.decoded_digits)
