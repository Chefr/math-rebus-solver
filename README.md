# math-rebus-solver

Mathematical rebus solver.

Solves mathematical rebuses of type "SEND + MORE = MONEY".

It may be useful if you need to find the answer to the rebus of the specified type or check the correctness of your own rebus.

## Examples

The Solver realize as a solution generator:
    
    solver = MathRebusSolver('EAT + THAT = APPLE')
    solutions = []
    limit = 10  # In case of a lot of solutions
    solution_generator = solver.get_solution_generator()
    type(solution_generator)  # generator
    for solution in solution_generator:
        solutions.append(solution)
        limit -= 1
        if limit == 0:
            break
    for solution in solutions:
        type(solution)  # mrebsolver.MathRebusSolution
        solution.decoded_equation  # '819 + 9219 = 10038'
        solutions.decoded_digits  # dict {'E': 8, 'A': 1 etc.}


This is probably not the most effective way to solve such rebuses, but by this decision I also wanted to demonstrate not the most usual use of the "flyweight" pattern.