from operator  import mul, add
from functools import reduce

from sympy.core               import Basic
from sympy.core               import Mul, Add

from sympde.calculus.core import BasicOperator
from symla.kronecker      import Kron, LinearOperator, Vector

#==============================================================================
class Dot(BasicOperator):
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

        if not len(_args) == 2:
            raise ValueError('Expecting one argument')
        
        args = _args
        args = list(args)
        originals = args.copy()

        # ...

        # ... treate the case where there is and Mul node
        mul_args = [arg for arg in args if isinstance(arg, Mul) and 
                    not all([isinstance(i, LinearOperator) for i in arg.args])]
        if mul_args:
            arg = mul_args[0]
            index = originals.index(arg)

            linops = [i for i in arg.args if isinstance(i, (LinearOperator, Kron, Vector, Add))]
            coeffs = [i for i in arg.args if i not in linops]

            linop = reduce(mul, linops)
            if len(coeffs) > 0:
                coeff = reduce(mul, coeffs)
            else:
                coeff = 1

            newargs = originals.copy()
            newargs[index] = linop
            return coeff*cls(*newargs)
        # ...

        add_args = [arg for arg in args if isinstance(arg, Add)]
        if add_args:
            arg = add_args[0]
            index = originals.index(arg)

            _args = []
            for i in arg.args:
                newargs = originals.copy()
                newargs[index] = i
                newexpr = cls(*newargs)
                _args.append(newexpr)

            return reduce(add, _args)

        return cls(*args, evaluate=False)

    def _hashable_content(self):
        return tuple(sorted(self._args, key= lambda x:x.__hash__()))

    def __hash__(self):
        h = self._mhash
        if h is None:
            h = hash((type(self).__name__,)) 
        return h
       
    def _sympystr(self, printer):
        sstr = printer.doprint
        return f'Dot({self.args[0]}, {self.args[1]})'
