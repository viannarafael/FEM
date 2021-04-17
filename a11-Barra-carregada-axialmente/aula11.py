import numpy as np 

#-----------------------------------
# Stiffnees matrix
def stiffness(E, A, L):
    k=np.asmatrix(np.zeros((2,2)))
    k[0,0]=1
    k[0,1]=-1
    k[1,0]=-1
    k[1,1]=1
    k=(E*A/L)*k
    return k
#-----------------------------------

#-----------------------------------
#Load vector
def load(qA, qB,L):
    q=np.asmatrix(np.zeros((2,1)))
    q[0,0] = qA
    q[1,0] = qB
    m=np.asmatrix(np.zeros((2,2)))
    m[0,0]=2
    m[0,1]=1
    m[1,0]=1
    m[1,1]=2
    m=(L/6.0)*m
    f=m*q
    return f
#-----------------------------------

#Input 
E = 10000.0 #Young`s modulus
A = 1.0     #area
L = 12.0    #bar length
c = 10.0    #load
nbars = 10  #number of bars

K=np.asmatrix(np.zeros((nbars+1,nbars+1)))
F=np.asmatrix(np.zeros((nbars+1,1)))

for n in range(nbars):
    
    #Assembly Stifness Matrix
    k = stiffness(E,A,L/nbars)
    K[n,n] = K[n,n] + k[0,0]
    K[n,n+1] = k[0,1]
    K[n+1,n] = k[1,0]
    K[n+1,n+1] = k[1,1]

    #Assembly Load Vector
    f=load(c*n*L/nbars,c*(n+1)*L/nbars,L/nbars)
    F[n,0]=F[n,0]+f[0,0]
    F[n+1,0]=F[n+1,0]+f[1,0]
#print(K)
#print(F)

#Reduced Matrix - Implementing restriction
Kr=np.asmatrix(np.zeros((nbars,nbars)))
Fr=np.asmatrix(np.zeros((nbars,1)))
for i in range(nbars):
    Fr [i,0]= F[i+1,0]
    for j in range(nbars):
        Kr [i,j]= K[i+1,j+1]

#Solve linear system
D = np.linalg.solve(Kr,Fr)

Dnew = np.asmatrix(np.zeros((nbars+1,1)))
for i in range(nbars):
    Dnew [i+1,0]= D[i,0]

print("For",nbars, "bars,\n\n D= \n")
print(Dnew)
