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
    assert(Inverse(a*b) == Inverse(b)*Inverse(a))
    assert(Inverse(a*b*c) == Inverse(c)*Inverse(b)*Inverse(a))
    assert(Inverse(a*b*c*d) == Inverse(d)*Inverse(c)*Inverse(b)*Inverse(a))

    assert(Inverse(alpha*a*b) == Inverse(b)*Inverse(a)/alpha)
    assert(Inverse(alpha*beta*a*b) == Inverse(b)*Inverse(a)/(alpha*beta))

    assert(Inverse(Kron(a,b)) == Kron(Inverse(a), Inverse(b)))
    assert(Inverse(Kron(a,b,c)) == Kron(Inverse(a), Inverse(b), Inverse(c)))
    assert(Inverse(Kron(a,b,c,d)) == Kron(Inverse(a), Inverse(b), Inverse(c), Inverse(d)))

    assert(Inverse(Kron(alpha*a,b)) == Kron(Inverse(a), Inverse(b))/alpha)
    assert(Inverse(Kron(alpha*a,beta*b)) == Kron(Inverse(a), Inverse(b))/(alpha*beta))
    assert(Inverse(Kron(alpha*a,beta*b,gamma*c)) == Kron(Inverse(a), Inverse(b), Inverse(c))/(alpha*beta*gamma))

    expr = Inverse(a+b)
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
