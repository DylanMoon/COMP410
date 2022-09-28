#!/usr/bin/env python3
#
# ---AST Definition---
#
# Exactly what a variable is is left abstract.
# In tests, variables are strings holding the name of the variable..
#
# There are three kinds of expressions:
#
# 1.) Literals, which represent the concept of a possibly
#     negated variable.  This is represented with the `Literal`
#     class.  The `variable` field holds the variable, and the
#     `is_positive` field holds `True` if it's a positive literal,
#     or `False` if its a negative literal.
#
# 2.) Logical and, which represents an AND operation between
#     two subexpressions.  This is represented with the `And`
#     class, which has `left` and `right` fields for subexpressions.
#
# 3.) Logical or, which represents an OR operation between
#     two subexpressions.  This is represented with the `Or`
#     class, which has `left` and `right` fields for subexpressions.
#
# A more compact representation of all the above information is shown
# below in a variant of a BNF grammar:
#
# x ∈ Variable
# b ∈ Boolean ::= True | False
# e ∈ Expression ::= Literal(x, b) | And(e1, e2) | Or(e1, e2)

class Literal:
    def __init__(self, variable, is_positive):
        self.variable = variable
        self.is_positive = is_positive

    def __str__(self):
        if self.is_positive:
            return self.variable
        else:
            return "!{}".format(self.variable)

class Binop:
    def __init__(self, left, right, op_string):
        self.left = left
        self.right = right
        self.op_string = op_string

    def __str__(self):
        return "({} {} {})".format(
            str(self.left),
            self.op_string,
            str(self.right))

class And(Binop):
    def __init__(self, left, right):
        super().__init__(left, right, "&&")

class Or(Binop):
    def __init__(self, left, right):
        super().__init__(left, right, "||")

# naive immutable map implementation
# just does a copy over an underlying dict
class ImmutableMap:
    def __init__(self, mapping = None):
        self.mapping = mapping if mapping is not None else dict()

    def add(self, key, value):
        new_mapping = self.mapping.copy()
        new_mapping[key] = value
        return ImmutableMap(new_mapping)

    def contains(self, key):
        return key in self.mapping

    def get(self, key):
        return self.mapping[key]

class List:
    def __init__(self):
        pass

class Nil(List):
    def __init__(self):
        super().__init__()

    def __str__(self):
        return "nil"

class Cons(List):
    def __init__(self, head, tail):
        super().__init__()
        self.head = head
        self.tail = tail
        
    def __str__(self):
        return "cons({}, {})".format(self.head, self.tail)


# add_literal
#
# Takes the following:
# 1.) An instance of `ImmutableMap` where the keys are variables and the
#     values are Python booleans (either `True` or `False`)
# 2.) A variable
# 3.) A Python boolean (either `True` or `False`)
#
# Returns:
# Either a new `ImmutableMap` containing the given variable/boolean binding,
# or None
#
# Purpose:
# Adds the given variable to the given `ImmutableMap` instance, mapping the
# variable to the given boolean. There are three cases of interest upon
# adding a variable to the `ImmutableMap` instance:
# 1.) The `ImmutableMap` instance does not contain the variable.  In this
#     case, the variable/boolean mapping is added, and the new `ImmutableMap`
#     instance is returned
# 2.) The `ImmutableMap` instance contains the variable, and it is mapped to
#     the same boolean as the one passed.  In this case, there is nothing that
#     needs to be added to the `ImmutableMap` instance, and so the
#     `ImmutableMap` instance is returned as-is.
# 3.) The `ImmutableMap` instance contains the variable, but it is mapped to
#     the opposite boolean as the one passed.  For example, the map contains
#     `False`, but the boolean passed was `True`. This means we hit a conflict:
#     a variable must be both true and false at the same time, which is
#     impossible.  As such, in this case None is returned.
#
# Do NOT modify add_literal.
#
def add_literal(immutable_map, variable, boolean):
    if immutable_map.contains(variable):
        if immutable_map.get(variable) == boolean:
            return immutable_map
        else:
            return None
    else:
        return immutable_map.add(variable, boolean)

# solve
#
# Takes the following:
# 1.) A `List` of expressions, using the linked list definition above.
#     `Nil` represents an empty list, and `Cons` represents a non-empty
#     list containing a `head` element followed by the rest of the list,
#     `tail`
# 2.) An `ImmutableMap` instance, where the keys are variables and the
#     values are Python booleans (either `True` or `False`)
#
# Returns:
# An `ImmutableMap` instance mapping variables to Python booleans
# corresponding to a satisfying solution, or None if there is no solution.
#
# Purpose:
# Uses semantic tableau (https://en.wikipedia.org/wiki/Method_of_analytic_tableaux)
# to try to find a satisfying solution.  The list of expressions represents expressions
# which must all be true for a satisfying solution.  The `ImmutableMap` instance
# represents truth values assigned so far for any literals.
#
# You need to implement solve.  To this end, the following hints may be helpful:
# 1.) solve needs to be recursive.
# 2.) If the list of expressions is empty (determinable by checking if `goals` is an
#     instance of `Nil`, as with `isinstance(goals, Nil)`), the given set of literals
#     represents a satisfying solution (that is, there is nothing left that
#     needs to be true).  This acts as your base case; all other cases are
#     recursive cases.
# 3.) If the list of expressions is non-empty (it's an instance of `Cons`), then
#     you'll need to see what kind of expression is first.  You can do this by
#     checking what kind of instance `goals.head` is; it could be a `Literal`,
#     `And`, or `Or`
# 4.) You will need to use `add_literal` in the case that you have a literal,
#     and return None (indicating an unsatisfiable solution) if add_literal returns
#     None.  You can check if the result is None with `result is None`, where `result`
#     is a variable to check.
# 5.) With or, you should try to solve with the left disjunct (the expression on
#     the left of the or) first.  If that returned None, then try with the right
#     disjunct instead.
# 6.) You do not need to write a lot of code; my reference solution is 23 lines long.
#     If you start needing a lot more code than that, ask for help to make sure
#     you're still on-track.
#

# Version for python 3.10 or later:

""" def solve(goals, literals):
    match goals:
        case Nil():
            return literals
        case Cons():
            match goals.head:
                case Literal():
                    return add_literal(literals, goals.head.variable, goals.head.is_positive)
                case And():
                    literals = solve(Cons(goals.head.left, Nil()), literals)
                    if literals is None: return None
                    return solve(Cons(goals.head.right, Nil()), literals)
                case Or():
                     return solve(Cons(goals.head.left, Nil()), literals) or solve(Cons(goals.head.right, Nil()), literals)
                case _:
                    return None
        case _:
            return None """

""" def solve(goals, literals):
    if isinstance(goals, Nil):
        return literals
    elif isinstance(goals, Cons):
        literals = solve(goals.head,literals)
        if literals is None: return None
        return solve(goals.tail, literals)
    elif isinstance(goals, Literal):
        literals = add_literal(literals, goals.variable, goals.is_positive)
        return literals
    elif isinstance(goals, And):
        literals = solve(goals.left, literals)
        if literals is None: return None
        literals = solve(goals.right, literals)
        return literals
    elif isinstance(goals, Or):
        literals_temp = literals
        literals_temp = solve(goals.left, literals_temp)
        return literals_temp or solve(goals.right, literals)
    else:
        return None """
            
def solve(goals, literals):
    if isinstance(goals, Nil): return literals
    if isinstance(goals, Cons):
        if isinstance(goals.head, Literal):
            literals = add_literal(literals, goals.head.variable, goals.head.is_positive)
        if isinstance(goals.head, And):
            literals = solve(Cons(goals.head.left, goals.tail), literals)
            if literals is None: return None
            literals = solve(Cons(goals.head.right, goals.tail), literals)
        if isinstance(goals.head, Or):
            literals_temp = solve(Cons(goals.head.left, goals.tail), literals)
            if literals_temp is None: return solve(Cons(goals.head.right, goals.tail), literals)
            return literals
        return solve(goals.tail, literals)
    return None

    #figure out why this is failing comutitive property


def solve_one(formula):
    return solve(Cons(formula, Nil()), ImmutableMap())

# tests that should be satisfiable
sat_tests = [And(Or(Literal("a", True),
                    Literal("b", False)),
                 Literal("b", True)), # (a || !b) && b
                 And(Or(Literal("b", False),
                    Literal("a", True)),
                 Literal("b", True)), # (!b || a) && b
             And(Or(Literal("x", True),
                    Literal("y", False)),
                 Or(Literal("y", False),
                    Literal("z", True))), # (x || !y) && (!y || z)
                    Or(And(Literal("x", False),Literal("x", True)), Literal("y", True)), # (!x && x) || y
                    Or(Literal("x", True), And(Literal("y", False), Literal("y", True)))] # x || (!y && y)

# tests that should be unsatisfiable
unsat_tests = [And(Literal("x", True),
                   Literal("x", False)), # x && !x
                   Or(And(Literal("x", False),Literal("x", True)), And(Literal("y", False), Literal("y", True)))] # (!x && x) || (!y && y)

def run_tests():
    tests_failed = False
    for test in sat_tests:
        if solve_one(test) is None:
            print("Failed: {}".format(test))
            print("\tWas UNSAT, should have been SAT")
            tests_failed = True

    for test in unsat_tests:
        if solve_one(test) is not None:
            print("Failed: {}".format(test))
            print("\tWas SAT, should have been UNSAT")
            tests_failed = True

    if not tests_failed:
        print("All tests passed")

if __name__ == "__main__":
    run_tests()
