from sympy import Symbol

from symla.kronecker import FiniteVectorSpace
from symla.kronecker import Matrix
from symla.kronecker import Kron
from symla.transpose   import Transpose

# ====================================================================
def test_transpose_1():
    V = FiniteVectorSpace('V')
    a, b, c, d = [Matrix(i, V, V) for i in ['a', 'b', 'c', 'd']]
    alpha, beta, gamma = [Symbol(i) for i in ['alpha', 'beta', 'gamma']]

    # .....................................
    assert(Transpose(a*b) == Transpose(b)*Transpose(a))
    assert(Transpose(a*b*c) == Transpose(c)*Transpose(b)*Transpose(a))
    assert(Transpose(a*b*c*d) == Transpose(d)*Transpose(c)*Transpose(b)*Transpose(a))

    assert(Transpose(alpha*a*b) == alpha * Transpose(b)*Transpose(a))
    assert(Transpose(alpha*beta*a*b) == (alpha*beta) * Transpose(b)*Transpose(a))

    assert(Transpose(Kron(a,b)) == Kron(Transpose(a), Transpose(b)))
    assert(Transpose(Kron(a,b,c)) == Kron(Transpose(a), Transpose(b), Transpose(c)))
    assert(Transpose(Kron(a,b,c,d)) == Kron(Transpose(a), Transpose(b), Transpose(c), Transpose(d)))

    assert(Transpose(Kron(alpha*a,b)) == alpha * Kron(Transpose(a), Transpose(b)))
    assert(Transpose(Kron(alpha*a,beta*b)) == (alpha*beta) * Kron(Transpose(a), Transpose(b)))
    assert(Transpose(Kron(alpha*a,beta*b,gamma*c)) == (alpha*beta*gamma) * Kron(Transpose(a), Transpose(b), Transpose(c)))
    
    # Transpose of Transpose
    assert(Transpose(Transpose(a)) == a)
    assert(Transpose(Transpose(Transpose(a))) == Transpose(a))
    assert(Transpose(a*b*Transpose(c)*d) == Transpose(d)*c*Transpose(b)*Transpose(a))
    
    # Transpose of Power
    assert(Transpose(a**alpha) == Transpose(a) ** alpha)



#######################################
if __name__ == '__main__':

    test_transpose_1()
