#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'Yee_172'
__date__ = '2017/8/28'

# from copy import deepcopy
from functools import reduce
from decimal import Decimal

def ftoi(num):
    """
    Float to int if it has no decimal
    1.0 -> 1
    """
    return int(num) if int(num) == num else num


def dtos(num):
    """
    Digit to Simply digit
    1.0000000000001 -> 1
    """
    return ftoi(round(num, 10))


def stos(string):
    """
    String to Simply digit
    '1.0000000000001' -> 1
    """
    return dtos(float(string))


class Indeterminate:
    """
    A member of the Term
    """

    def __init__(self, unknown, subscript=None, degree=1.0):
        if not isinstance(unknown, str):
            raise Exception('Name of Indeterminate must be string!')
        if not isinstance(subscript, str) and subscript is not None:
            raise Exception('Subscript must be string!')
        if isinstance(degree, bool) or isinstance(degree, str):
            raise Exception('Degree must be int or float!')

        if degree:
            self.unknown = unknown
            self.subscript = subscript
            self.degree = dtos(degree)
        else:
            self.unknown = ''
            self.subscript = None
            self.degree = 0

    def tolist(self):
        """
        Return a list of its info
        """
        return [self.unknown, self.subscript, self.degree]

    def __str__(self):
        """
        Return a string means the same
        """
        if not self.unknown:
            return '1'
        elif self.degree == 1:
            if self.subscript:
                return '%s_%s' % (self.unknown, self.subscript)
            else:
                return self.unknown
        else:
            if self.subscript:
                return '%s_%s^%s' % (self.unknown, self.subscript, str(self.degree))
            else:
                return '%s^%s' % (self.unknown, str(self.degree))

    def latex(self):
        """
        Return a latex form
        """
        if not self.unknown:
            return '1'
        elif self.degree == 1:
            if self.subscript:
                return '%s$_{%s}$' % (self.unknown, self.subscript)
            else:
                return self.unknown
        else:
            if self.subscript:
                return '%s$_{%s}^{%s}$' % (self.unknown, self.subscript, str(self.degree))
            else:
                return '%s$^{%s}$' % (self.unknown, str(self.degree))

    def showdetail(self, spaces=0):
        """
        Print detailed info
        """
        if not isinstance(spaces, int):
            raise Exception('The number of spaces must be integer!')

        print(' ' * spaces + 'unknown  :\t    %s' % self.unknown)
        print(' ' * spaces + 'subscript:\t    %s' % self.subscript)
        print(' ' * spaces + 'degree   :\t    %s' % str(self.degree))

    def __eq__(self, other):
        """
        Judge if two Indeterminates are equal
        """
        if not isinstance(other, Indeterminate):
            raise Exception('Must compare with an Indeterminate!')

        if self.unknown == other.unknown:
            if self.subscript == other.subscript:
                if self.degree == other.degree:
                    return True
        return False

    # def __copy__(self):
    #     """
    #     Return a copy of itself
    #     """
    #     return Indeterminate(self.unknown, self.subscript, self.degree)

    def ismultiplicative(self, other):
        """
        Judge if two Indeterminates can multiply
        """
        if not isinstance(other, Indeterminate):
            raise Exception('Must compare with an Indeterminate!')

        if self == CONSTANT or other == CONSTANT:
            return True
        if self.unknown == other.unknown:
            if self.subscript == other.subscript:
                return True
        return False

    def __mul__(self, other):
        """
        Multiply two multiplicative Indeterminates
        I1 * I2
        """
        if not isinstance(other, Indeterminate):
            raise Exception('Indeterminate must be valid!')
        if not self.ismultiplicative(other):
            raise Exception('Multiplicative Indeterminate acquired!')

        if self == CONSTANT:
            return Indeterminate(other.unknown, other.subscript, other.degree)
        degree = self.degree + other.degree
        return Indeterminate(self.unknown, self.subscript, degree) if degree else CONSTANT

    def __truediv__(self, other):
        """
        Divide an Indeterminate by another
        I1 / I2
        """
        return self * Indeterminate(other.unknown, other.subscript, -other.degree)


CONSTANT = Indeterminate('', degree=0)


class Term:
    """
    A member of the Polynomial
    """

    def __init__(self, *indeterminates, coefficient=1.0):
        if isinstance(coefficient, bool) or isinstance(coefficient, str):
            raise Exception('Coefficient must be valid!')
        for each in indeterminates:
            if not isinstance(each, Indeterminate):
                raise Exception('Each Indeterminate must be valid!')

        # Sort the indeterminates by indeterminate and subscript
        indeterminates = sorted(indeterminates, key=lambda x: x.subscript or '')
        indeterminates = sorted(indeterminates, key=lambda x: x.unknown)
        index = 0
        while 1:
            if index >= len(indeterminates) - 1:
                break
            try:
                middle = indeterminates[index] * indeterminates[index + 1]
                if middle == CONSTANT:
                    indeterminates = indeterminates[:index] + indeterminates[index + 2:]
                else:
                    indeterminates = indeterminates[:index] + [middle] + indeterminates[index + 2:]
            except:
                index += 1

        if coefficient:
            self.indeterminates = indeterminates or [CONSTANT]
            self.coefficient = dtos(coefficient)
            self.degree = dtos(sum(each.degree for each in indeterminates))
        else:
            self.indeterminates = [CONSTANT]
            self.coefficient = 0
            self.degree = 0

    def tolist(self):
        """
        Return a list of its info
        """
        return [[each.tolist() for each in self.indeterminates], self.coefficient, self.degree]

    def __str__(self):
        """
        Return a string means the same
        """
        if not self.degree:
            return '%s' % str(self.coefficient)
        else:
            string = '' if self.coefficient == 1 else '-' if self.coefficient == -1 else str(self.coefficient)
            string += '*'.join(str(each) for each in self.indeterminates)
            return string

    def latex(self):
        """
        Return a latex form
        """
        if not self.degree:
            return '%s' % str(self.coefficient)
        else:
            string = '' if self.coefficient == 1 else '-' if self.coefficient == -1 else str(self.coefficient)
            string += ''.join(each.latex() for each in self.indeterminates)
            return string

    def showdetail(self, spaces=0):
        """
        Print detailed info
        """
        print(' ' * spaces + 'number of Indeterminates:\t    %d' % len(self.indeterminates))
        print(' ' * spaces + 'coefficient             :\t    %s' % str(self.coefficient))
        print(' ' * spaces + 'degree                  :\t    %s' % str(self.degree))
        for n, each in enumerate(self.indeterminates):
            print(' ' * spaces + 'Indeterminate #%02d:' % (n + 1))
            each.showdetail(5 + spaces)

    def __eq__(self, other):
        """
        Judge if two Terms are equal
        """
        if not isinstance(other, Term):
            raise Exception('Must compare with a Term!')

        if self.coefficient == other.coefficient:
            if self.degree == other.degree:
                if self.indeterminates == other.indeterminates:
                    return True
        return False

    def isincreasable(self, other):
        """
        Judge if two Terms is increasable
        """
        if not isinstance(other, Term):
            raise Exception('Must compare with a Term!')

        if self == ZERO_TERM or other == ZERO_TERM:
            return True
        if self.degree == other.degree:
            if len(self.indeterminates) == len(other.indeterminates):
                for n, each in enumerate(other.indeterminates):
                    if self.indeterminates[n] != each:
                        return False
                return True
        return False

    def __neg__(self):
        """
        Return negative Term
        - T1
        """
        return Term(*self.indeterminates, coefficient=-self.coefficient)

    def __add__(self, other):
        """
        Add two Terms
        T1 + T2
        """
        if not isinstance(other, Term):
            raise Exception('Must add with a Term!')
        if not self.isincreasable(other):
            raise Exception('Increasable Term acquired!')

        if self == ZERO_TERM:
            return Term(*other.indeterminates, coefficient=other.coefficient)
        return Term(*self.indeterminates, coefficient=self.coefficient + other.coefficient)

    def __sub__(self, other):
        """
        Subtract two Terms
        T1 - T2
        """
        return -other + self

    def __mul__(self, other):
        """
        Multiply two Terms
        T1 * T2
        """
        if not isinstance(other, Term):
            raise Exception('Term acquired')

        indeterminates = self.indeterminates + other.indeterminates
        return Term(*indeterminates, coefficient=self.coefficient * other.coefficient)

    def __truediv__(self, other):
        """
        Divide two Terms
        T1 / T2
        """
        return self * Term(*[CONSTANT / each for each in other.indeterminates], coefficient=1 / other.coefficient)


ZERO_TERM = Term(coefficient=0)


class Polynomial:
    """
    A set of terms
    """

    def __init__(self, *terms):
        for each in terms:
            if not isinstance(each, Term):
                raise Exception('Each Term must be valid!')

        # Sort the terms by degree and number of Indeterminates
        terms = sorted(terms, key=lambda x: str(Term(*x.indeterminates)))
        terms = sorted(terms, key=lambda x: len(x.indeterminates))
        terms = sorted(terms, key=lambda x: x.degree, reverse=True)
        index = 0
        while 1:
            if index >= len(terms) - 1:
                break
            try:
                middle = terms[index] + terms[index + 1]
                if middle == ZERO_TERM:
                    terms = terms[:index] + terms[index + 2:]
                else:
                    terms = terms[:index] + [middle] + terms[index + 2:]
            except:
                index += 1

        terms = terms or [ZERO_TERM]
        self.terms = terms
        self.degree = terms[0].degree

    def tolist(self):
        """
        Return a list of its info
        """
        return [[each.tolist() for each in self.terms], self.degree]

    def __str__(self):
        """
        Return a string means the same
        """
        string = '+'.join(str(each) for each in self.terms).replace('+-', '-')
        return string[1:] if string[0] == '+' else string

    def latex(self):
        """
        Return a latex form
        """
        string = '+'.join(each.latex() for each in self.terms).replace('+-', '-')
        return string[1:] if string[0] == '+' else string

    def showdetail(self, spaces=0):
        """
        Print detailed info
        """
        print(' ' * spaces + 'number of Terms:\t    %d' % len(self.terms))
        print(' ' * spaces + 'degree         :\t    %s' % str(self.degree))
        for n, each in enumerate(self.terms):
            print(' ' * spaces + 'Term #%02d:' % (n + 1))
            each.showdetail(5 + spaces)

    def __eq__(self, other):
        """
        Judge if two Polynomials are equal
        P1 == P2
        """
        if not isinstance(other, Polynomial):
            raise Exception('Must compare with a Polynomial!')

        if self.terms == other.terms:
            return True
        return False

    def __neg__(self):
        """
        Return negative Polynomial
        - P1
        """
        return Polynomial(*[-each for each in self.terms])

    def __add__(self, other):
        """
        Add polynomials together
        P1 + P2
        """
        if not isinstance(other, Polynomial):
            if not isinstance(other, int):
                if not isinstance(other, float):
                    raise Exception('Each Polynomial must be valid!')

        try:
            other = Polynomial(Term(CONSTANT, coefficient=other))
        finally:
            terms = self.terms + other.terms
            return Polynomial(*terms)

    __radd__ = __add__

    def __sub__(self, other):
        """
        Subtract two Polynomials
        P1 - P2
        """
        if not isinstance(other, Polynomial):
            if not isinstance(other, int):
                if not isinstance(other, float):
                    if not isinstance(other, Decimal):
                        raise Exception('Each Polynomial must be valid!')

        try:
            other = Polynomial(Term(CONSTANT, coefficient=other))
        finally:
            return -other + self

    def __rsub__(self, other):
        """
        Constant minus Polynomial
        P2 - P1
        """
        if not isinstance(other, int) and not isinstance(other, float):
            raise Exception('Valid constant required!')

        return -self + other

    def __mul__(self, other):
        """
        Multiply two Polynomials
        P1 * P2
        """
        if not isinstance(other, Polynomial):
            if not isinstance(other, int):
                if not isinstance(other, float):
                    if not isinstance(other, Decimal):
                        raise Exception('Each Polynomial must be valid!')

        try:
            other = Polynomial(Term(CONSTANT, coefficient=other))
        finally:
            terms = []
            for each in other.terms:
                terms += [_each * each for _each in self.terms]
            return Polynomial(*terms)

    __rmul__ = __mul__

    def __truediv__(self, other):
        """
        Divide two Polynomials
        P1 / P2
        """
        if not isinstance(other, int) and not isinstance(other, float) and not isinstance(other, Decimal):
            raise Exception('Not supported yet!')
        try:
            return self * (1 / other)
        except:
            raise Exception('Valid constant required!')
        # TODO __truediv__

    def __pow__(self, power, modulo=None):
        """
        Power a Polynomial
        P1 ** power
        """
        if not isinstance(power, int) or power < 0:
            raise Exception('Power must be nonnegative integer!')

        return reduce(lambda x, y: x * y, [self] * power, 1)


# ---[test zone]---
# a = Indeterminate('x', subscript='1', degree=1)
# b = Indeterminate('y', subscript='3', degree=2)
# c = Indeterminate('x', subscript='2', degree=4)
# d = Indeterminate('x', subscript='1', degree=1)
# T1 = Term(a, b, c, a, coefficient=5)
# T2 = Term(a, a, b, coefficient=3)
# T3 = Term(c, c, coefficient=4)
# T4 = Term(coefficient=-1)
# T5 = Term(a, b, d)
# P1 = Polynomial(T2, T1, T3, T4)
# P2 = Polynomial(T2, T3)
# print(P1.latex())
