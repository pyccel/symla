from sympy import Symbol

from symla.kronecker import FiniteVectorSpace
from symla.kronecker import Matrix
from symla.kronecker import Vector
from symla.dot   import Dot
from symla.transpose   import Transpose

# ====================================================================
def test_dot_1():
    V = FiniteVectorSpace('V')
    u, v, w = [Vector(c,V) for c in ['u','v', 'w']]
    alpha, beta, gamma = [Symbol(i) for i in ['alpha', 'beta', 'gamma']]
    # .....................................
    assert(Dot(alpha*v,beta*u) == alpha*beta*Dot(v,u))
    assert(Dot(alpha*(v+w),beta*u) == alpha*beta*(Dot(v,u) + Dot(w,u)))
    assert(Dot(u,v) == Dot(v,u))
    assert(Dot(u,v) - Dot(v,u) == 0)
    assert(Dot(u,v) + Dot(v,u) == 2*Dot(v, u))
    assert(Dot(u,u) +2*Dot(u,v) + Dot(v,v) == Dot(u+v,u+v))


#######################################
if __name__ == '__main__':

    test_dot_1()
