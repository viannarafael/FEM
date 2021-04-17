import numpy as np
from bar_axial_load import solve

#Load vector
def equivalentload(qA, qB,L):
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

#Input 
E = 10000.0 #Young`s modulus
A = 1.0     #area
L = 12.0    #bar length
c = 10.0    #load
nbars = 10  #number of bars
nnodes=nbars+1


#Matriz de coordenads
coords=np.asmatrix(np.zeros((nnodes,1)))
for n in range(nnodes):
    coords[n]=n*L/nbars

#Matriz de conectividade
connect=np.asmatrix(np.zeros((nbars,2)))
for elem in range(nbars):
    connect[elem,0]=elem
    connect[elem,1]=elem+1

#Matriz de restricoes
restr=np.asmatrix(np.zeros((nnodes,1)))
restr[0,0]=1

#Matriz de Propriedades
prop=np.asmatrix(np.zeros((nbars,2)))
for elem in range (nbars):
    prop[elem,0] = E
    prop[elem,1] = A

#Vetor de Cargas
load=np.asmatrix(np.zeros((nbars+1,1)))
for n in range(nbars):
    f=equivalentload(c*n*L/nbars,c*(n+1)*L/nbars,L/nbars)
    load[n,0]=load[n,0]+f[0,0]
    load[n+1,0]=load[n+1,0]+f[1,0]
    
print("coords =\n",coords)
print("\nconnect =\n",connect)
print("\nload =\n",load)
print("\nrestr =\n",restr)
print("\nprop =\n",prop)

D = solve(coords, connect, restr, prop, load)