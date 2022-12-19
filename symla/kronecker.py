from operator  import mul, add
from functools import reduce

from sympy                    import Symbol
from sympy                    import Matrix as sp_Matrix
from sympy                    import ImmutableDenseMatrix
from sympy                    import cacheit
from sympy.core               import Basic
from sympy.core               import Add, Mul, Expr

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
    def __new__(cls, name, dimension=None, field=None):

        obj = Basic.__new__(cls)
        obj._name  = name
        obj._dimension = dimension
        obj._field = field

        return obj

    @property
    def name(self):
        return self._name

    @property
    def dimension(self):
        return self._dimension

    @property
    def field(self):
        return self._field
    
    @property
    def dtype(self):
        # TODO assign a data type for each field
        pass

    def _sympystr(self, printer):
        sstr = printer.doprint
        return sstr(self.name)

    def __mul__(self, other):
        raise NotImplementedError('TODO')

    def __hash__(self):
        return hash((self.name, self._dimension, self._field))

#==============================================================================
# TODO improve
class Vector(Symbol):
    def __new__(cls, name, space=None, **assumptions):
        obj = Symbol.__new__(cls, name)
        obj._space = space
        obj._discretizable = False
        if assumptions.get('values'):
            obj._values = assumptions.get('values')
            # TODO validate values type and shape
            obj._discretizable = True

        return obj
    
    @property
    def shape(self):
        return None if self._space == None else self._space.dimension()

    @property
    def dtype(self):
        return None if self._space == None else self._space.dtype()
    


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
# TODO treat the Zero case
class Kron(BasicOperator):
    """
    """

    def __new__(cls, *args, **options):
        # (Try to) sympify args first
        if options.pop('evaluate', True):
            args = [arg.expand() for arg in args]
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

        if len(_args) <= 1:
            raise ValueError('Expecting at least two arguments')

        args = _args

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
        mul_args = [arg for arg in args if isinstance(arg, Mul) and 
                    not all([isinstance(i, LinearOperator) for i in arg.args])]
        if mul_args:
            arg = mul_args[0]
            index = originals.index(arg)

            linops = [i for i in arg.args if isinstance(i, (LinearOperator, Kron))]
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

        return cls(*args, evaluate=False)
