from sympy                    import Symbol

from symla.kronecker import FiniteVectorSpace
from symla.kronecker import Matrix
from symla.kronecker import Kron

# ====================================================================
def test_kronecker_1():
    V = FiniteVectorSpace('V')
    a, b, c, d = [Matrix(i, V, V) for i in ['a', 'b', 'c', 'd']]
    alpha, beta, gamma = [Symbol(i) for i in ['alpha', 'beta', 'gamma']]

    # .....................................
    # Kron can be called without evaluation
    assert(not(Kron(a, b+c, evaluate=False) == Kron(a,b) + Kron(a,c)))

    # Distributivity
    assert(Kron(a, b+c) == Kron(a,b) + Kron(a,c))
    assert(Kron(a+b, c) == Kron(a,c) + Kron(b,c))
    assert(Kron(a, beta*b) == beta * Kron(a,b))
    assert(Kron(alpha*a, b) == alpha * Kron(a,b))
    assert(Kron(alpha*a, beta*b) == alpha * beta * Kron(a,b))
    assert(Kron(alpha*a,beta*b+gamma*c) == alpha*beta*Kron(a, b) + alpha*gamma*Kron(a, c) )
    assert(Kron(alpha*a+beta*b,gamma*c) == alpha*gamma*Kron(a, c) + beta*gamma*Kron(b, c) )

    # Mixed Product
    assert(Kron(alpha*a, beta*b*c) == alpha*beta*Kron(a, b*c))

    # Associativity
    assert(Kron(a, Kron(b,c)) == Kron(a,b,c))
    assert(Kron(Kron(a,b), c) == Kron(a,b,c))
    assert(Kron(Kron(a+b,d), Kron(b,c)) == Kron(a, d, b, c) + Kron(b, d, b, c))
    # .....................................

#######################################
if __name__ == '__main__':

    test_kronecker_1()

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
