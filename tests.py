import unittest
from mrebsolver import MathRebusSolver


class MathRebusSolverTest(unittest.TestCase):

    def test_add(self):
        solver = MathRebusSolver('EAT + THAT = APPLE')
        solutions = []
        limit = 2
        for solution in solver.get_solution_generator():
            solutions.append(solution)
            limit -= 1
            if limit == 0:
                break
        self.assertEqual(len(solutions), 1)
        self.assertEqual(solutions[0].decoded_equation, '819 + 9219 = 10038')
        self.assertEqual(solutions[0].decoded_digits,
                         {'E': 8, 'A': 1, 'T': 9, 'H': 2, 'P': 0, 'L': 3})

    def test_sub(self):
        self.assertEqual(__class__._calculate('AB - C = 1', 2),
                         ['10 - 9 = 1'])

    def test_all_answers(self):
        self.assertEqual(__class__._calculate('-AB + BC = AA', 10),
                         ['- 12 + 23 = 11', '- 24 + 46 = 22', '- 36 + 69 = 33',
                          '- 37 + 70 = 33', '- 49 + 93 = 44'])

    def test_multiply(self):
        self.assertEqual(__class__._calculate('TWO * TWO  = THREE', 2),
                         ['138 * 138 = 19044'])

    def test_division(self):
        self.assertEqual(__class__._calculate('AB / BC = 9', 2),
                         ['91 / 10 = 9'])

    def test_brackets(self):
        self.assertEqual(__class__._calculate(
            '1A - (2 + (3*2) - 4/2) = B2',
            2),
            ['18 - ( 2 + ( 3 * 2 ) - 4 / 2 ) = 12'])

    def test_multiply_solutions(self):
        self.assertEqual(__class__._calculate('A + B  = CD', 5),
                         ['2 + 8 = 10', '3 + 7 = 10', '3 + 9 = 12',
                          '4 + 6 = 10', '4 + 8 = 12'])

    def test_number(self):
        self.assertEqual(__class__._calculate('NO + 4 = YES', 2),
                         ['98 + 4 = 102'])

    def test_multiple_numbers(self):
        self.assertEqual(__class__._calculate('5 + A = 12', 2),
                         ['5 + 7 = 12'])

    def test_cyrillic(self):
        self.assertEqual(__class__._calculate('УДАР + УДАР = ДРАКА', 2),
                         ['8126 + 8126 = 16252'])

    def test_no_result(self):
        self.assertEqual(__class__._calculate('AB - BC = AA', 2), [])

    def test_errors(self):
        self.assertRaises(IOError, __class__._calculate, '*AB + CD = HH', 2)
        self.assertRaises(IOError, __class__._calculate, 'AB + CD( = HH', 2)
        self.assertRaises(IOError, __class__._calculate, 'AB + / CD = HH', 2)
        self.assertRaises(IOError, __class__._calculate, 'AB + - CD( = HH', 2)
        self.assertRaises(IOError, __class__._calculate, 'AB + CD = HH +', 2)
        self.assertRaises(IOError, __class__._calculate, 'CD - AA) = HH', 2)

    @staticmethod
    def _calculate(rebus, limit):
        solver = MathRebusSolver(rebus)
        decoded_equations = []
        for solution in solver.get_solution_generator():
            decoded_equations.append(solution.decoded_equation)
            limit -= 1
            if limit == 0:
                break
        return decoded_equations


if __name__ == '__main__':
    unittest.main()
