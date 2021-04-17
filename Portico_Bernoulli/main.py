import numpy as np
from solver_bernoulli import *
from desenhamalha import *

#Input 
E = 1            #Young`s modulus
A = 300000            #Cross sectional area
I = 32400
nnodes = 4
nelem = 3

#Matriz de coordenadas
coords=np.asmatrix(np.zeros((nnodes,2)))
coords[0,:]= [0,0]
coords[1,:]= [0,4]
coords[2,:]= [4,3]
coords[3,:]= [4,0]

#Matriz de conectividade
connect=np.asmatrix(np.zeros((nelem,2)))
connect[0,:]=[1,2]
connect[1,:]=[2,3]
connect[2,:]=[3,4]

# Matriz de restricoes
restr=np.asmatrix(np.zeros((nnodes,3)))
restr[0,:]=[1,1,1]
restr[3,:]=[1,1,1]

#Matriz de Propriedades
prop=np.asmatrix(np.zeros((nelem,3)))
for elem in range (nelem):
    prop[elem,:] = [E,A,I]

#Vetor de Cargas
load=np.asmatrix(np.zeros((nnodes,3)))
load[1,:]=[100,0,0]
load[2,:]=[0,0,-20]

#Solver
D = solver_bernoulli(coords, connect, restr, prop, load)
print(D)

#Desenha Malha
Plot_Model(coords, connect, restr, load)
D=np.reshape(D,(nnodes,2))
Plot_Deformada(coords-100000*D, connect, restr, load)
