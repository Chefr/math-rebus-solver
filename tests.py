import unittest
from mrebsolver import MathRebusSolver


class MathRebusSolverTest(unittest.TestCase):

    def test_common_add(self):
        solver = MathRebusSolver('EAT + THAT = APPLE')
        solutions = []
        limit = 10
        for solution in solver.get_solution_generator():
            solutions.append(solution.decoded_equation)
            limit -= 1
            if limit == 0:
                break
        self.assertEqual(solutions, ['819 + 9219 = 10038'])

    def test_common_multiply(self):
        solver = MathRebusSolver('TWO * TWO  = THREE')
        solutions = []
        limit = 10
        for solution in solver.get_solution_generator():
            solutions.append(solution.decoded_equation)
            limit -= 1
            if limit == 0:
                break
        self.assertEqual(solutions, ['138 * 138 = 19044'])

    def test_multiply_solutions(self):
        solver = MathRebusSolver('A + B  = CD')
        solutions = []
        limit = 10
        for solution in solver.get_solution_generator():
            solutions.append(solution.decoded_equation)
            limit -= 1
            if limit == 0:
                break
        self.assertEqual(solutions, ['2 + 8 = 10',
                                     '3 + 7 = 10',
                                     '3 + 9 = 12',
                                     '4 + 6 = 10',
                                     '4 + 8 = 12',
                                     '4 + 9 = 13',
                                     '5 + 7 = 12',
                                     '5 + 8 = 13',
                                     '5 + 9 = 14',
                                     '6 + 4 = 10'
                                     ])

    def test_multiple_numbers(self):
        solver = MathRebusSolver('5 + A = 12')
        solutions = []
        limit = 2
        for solution in solver.get_solution_generator():
            solutions.append(solution.decoded_equation)
            limit -= 1
            if limit == 0:
                break
        self.assertEqual(solutions, ['5 + 7 = 12'])

    def test_number(self):
        solver = MathRebusSolver('NO + 4 = YES')
        solutions = []
        limit = 2
        for solution in solver.get_solution_generator():
            solutions.append(solution.decoded_equation)
            limit -= 1
            if limit == 0:
                break
        self.assertEqual(solutions, ['98 + 4 = 102'])

    def test_cyrillic(self):
        solver = MathRebusSolver('УДАР + УДАР = ДРАКА')
        solutions = []
        limit = 2
        for solution in solver.get_solution_generator():
            solutions.append(solution.decoded_equation)
            limit -= 1
            if limit == 0:
                break
        self.assertEqual(solutions, ['8126 + 8126 = 16252'])


if __name__ == '__main__':
    unittest.main()
