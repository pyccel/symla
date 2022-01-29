from operator  import mul, add
from functools import reduce

from sympy                    import Indexed, sympify, Symbol
from sympy                    import Matrix as sp_Matrix
from sympy                    import ImmutableDenseMatrix
from sympy                    import cacheit
from sympy.core               import Basic
from sympy.core               import Add, Mul, Pow, Expr
from sympy.core.containers    import Tuple
from sympy.core.singleton     import S
from sympy.core.decorators    import call_highest_priority
from sympy.core.compatibility import is_sequence

from sympde.calculus.core import BasicOperator
from symla.kronecker      import Kron, LinearOperator

#==============================================================================
class Inverse(BasicOperator):
    """
    """
    def __new__(cls, *args, **options):
        # (Try to) sympify args first

        if options.pop('evaluate', True):
            r = cls.eval(*args)
        else:
            r = None

        if r is None:
            return Basic.__new__(cls, *args, **options)
        else:
            return r

    @classmethod
    def eval(cls, *_args):

        if not _args:
            return

        if not len(_args) == 1:
            raise ValueError('Expecting one argument')

        expr = _args[0]

        if isinstance(expr, Kron):
            args = [cls(a, evaluate=False) for a in expr.args]
            return Kron(*args)

        elif isinstance(expr, Mul):
            linops = [i for i in expr.args if isinstance(i, (LinearOperator, Kron))]
            coeffs = [i for i in expr.args if i not in linops]

            linops = [cls(i) for i in linops]
            linop = reduce(mul, linops[::-1])
            if len(coeffs) > 0:
                coeff = reduce(mul, coeffs)
            else:
                coeff = 1

            return linop / coeff

        return cls(expr, evaluate=False)

    def _sympystr(self, printer):
        sstr = printer.doprint
        return 'Inverse({arg})'.format(arg=sstr(self.args[0]))
