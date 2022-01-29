from sympy import Symbol

from symla.kronecker import FiniteVectorSpace
from symla.kronecker import Matrix
from symla.kronecker import Kron
from symla.inverse   import Inverse

# ====================================================================
def test_inverse_1():
    V = FiniteVectorSpace('V')
    a, b, c, d = [Matrix(i, V, V) for i in ['a', 'b', 'c', 'd']]
    alpha, beta, gamma = [Symbol(i) for i in ['alpha', 'beta', 'gamma']]

    # .....................................
    expr = Inverse(a)
#    expr = Inverse(Kron(a,b))
    print(expr)

#######################################
if __name__ == '__main__':

    test_inverse_1()

    # .....................................
#    # TODO not working
#    expr = Kron(a+d*a, beta*b*c)
#    print(expr)
#    print('')

#    # TODO not working
#    expr = Kron(alpha*a,Kron(b, gamma*c) + Kron(beta*b,d))
#    print(expr)
#    print('')
    # .....................................
