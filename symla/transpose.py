from operator  import mul
from functools import reduce

from sympy.core               import Basic
from sympy.core               import Add, Mul, Pow

from sympde.calculus.core import BasicOperator
from symla.kronecker      import Kron, LinearOperator

#==============================================================================
class Transpose(BasicOperator):
    """
    """
    def __new__(cls, *args, **options):
        # (Try to) sympify args first

        if options.pop('evaluate', True):
            args = [arg.expand() if hasattr(arg, 'expand') else arg
                    for arg in args]
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
        
        if isinstance(expr, Transpose):
            return _args[0].args[0]

        if isinstance(expr, Kron):
            args = [cls(a, evaluate=False) for a in expr.args]
            return Kron(*args)

        elif isinstance(expr, Pow):
            return cls(expr.base) ** expr.exp
        
        elif isinstance(expr, Add):
            return reduce(Add, [cls(arg) for arg in expr.args])

        elif isinstance(expr, Mul):
            linops = [i for i in expr.args if isinstance(i, (LinearOperator, Kron, Transpose))]
            coeffs = [i for i in expr.args if i not in linops]

            linops = [cls(i) for i in linops]
            linop = reduce(mul, linops[::-1])
            if len(coeffs) > 0:
                coeff = reduce(mul, coeffs)
            else:
                coeff = 1

            return coeff * linop

        return cls(expr, evaluate=False)

    def _sympystr(self, printer):
        sstr = printer.doprint
        return 'Trans({arg})'.format(arg=sstr(self.args[0]))
