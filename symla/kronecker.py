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

#==============================================================================
@cacheit
def has(obj, types):
    if hasattr(obj, 'args'):
        return isinstance(obj, types) or any(has(i, types) for i in obj.args)
    else:
        return isinstance(obj, types)

@cacheit
def is_zero(x):
    if isinstance(x, (sp_Matrix, ImmutableDenseMatrix)):
        return all( i==0 for i in x[:])
    else:
        return x == 0

#==============================================================================
class FiniteVectorSpace(Basic):
    """
    """
    def __new__(cls, name, shape=None):

        obj = Basic.__new__(cls)
        obj._name  = name
        obj._shape = shape

        return obj

    @property
    def name(self):
        return self._name

    @property
    def shape(self):
        return self._shape

    def _sympystr(self, printer):
        sstr = printer.doprint
        return sstr(self.name)

    def __mul__(self, other):
        raise NotImplementedError('TODO')

    def __hash__(self):
        return hash((self.name, self.shape))

#==============================================================================
# TODO improve
class Vector(Symbol):
    pass

#==============================================================================
class LinearOperator(Symbol):
    def __new__(cls, name, domain, codomain):
        if not isinstance(domain, FiniteVectorSpace):
            raise ValueError('Expecting a FiniteVectorSpace')

        if not isinstance(codomain, FiniteVectorSpace):
            raise ValueError('Expecting a FiniteVectorSpace')

        obj = Expr.__new__(cls)
        obj._name = name
        obj._domain = domain
        obj._codomain = codomain

        return obj

    @property
    def name(self):
        return self._name

    @property
    def domain(self):
        return self._domain

    @property
    def codomain(self):
        return self._codomain

    def _sympystr(self, printer):
        sstr = printer.doprint
        return sstr(self.name)

    def __hash__(self):
        return hash((self.name, self.domain, self.codomain))

#==============================================================================
class Matrix(LinearOperator):
    pass

#==============================================================================
class Kron(BasicOperator):
    """
    """
    is_scalar      = False
    is_commutative = False

    def __new__(cls, *args, **options):

        # If one argument is the zero vector, return 0
        # TODO treat the Zero case
#        if any([is_zero(arg) for arg in args]):
#            return S.Zero

        krons = [i for i in args if isinstance(i, Kron)]
        if krons:
            newargs = list(args).copy()
            for kron in krons:
                index = newargs.index(kron)
                newargs = newargs[:index] + list(kron.args) + newargs[index+1:]
            return cls(*newargs)

        if all([isinstance(i, LinearOperator) for i in args]):
            return Basic.__new__(cls, *args)

        if all([ isinstance(arg, LinearOperator) or
                (isinstance(arg, Mul) and all([isinstance(i, LinearOperator) for i in arg.args]))
                for arg in args]):
            return Basic.__new__(cls, *args)

        evaluate = options.pop('evaluate', True)
        if not evaluate:
            return Basic.__new__(cls, *args)

        args = list(args)
        originals = args.copy()

        # ... treate the case where there is and Add node
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
        # ...

        # ... treate the case where there is and Mul node
        mul_args = [arg for arg in args if isinstance(arg, Mul)]
        if mul_args:
            arg = mul_args[0]
            index = originals.index(arg)

            linops = [i for i in arg.args if isinstance(i, LinearOperator)]
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

        return cls(*args)
