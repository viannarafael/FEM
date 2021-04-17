import numpy as np
from matplotlib import pyplot as plt
from solver import *
from desenhamalha import *

#Input 
E = 210e6         #Young`s modulus
A = 5*10e-3            #Cross sectional area
nnodes= 4
nelem=3

#Matriz de coordenadas
coords=np.asmatrix(np.zeros((nnodes,2)))
coords[0,:]= [4,5]
coords[1,:]= [0,0]
coords[2,:]= [4,0]
coords[3,:]= [8,0]

#Matriz de conectividade
connect=np.asmatrix(np.zeros((nelem,2)))
connect[0,:]=[1,2]
connect[1,:]=[1,3]
connect[2,:]=[1,4]

# Matriz de restricoes
restr=np.asmatrix(np.zeros((nnodes,2)))
restr[1,:]=[1,1]
restr[2,:]=[1,1]
restr[3,:]=[1,1]

#Matriz de Propriedades
prop=np.asmatrix(np.zeros((nelem,2)))
for elem in range (nelem):
    prop[elem,:] = [E,A]

#Vetor de Cargas
load=np.asmatrix(np.zeros((nnodes,2)))
load[0,:]=[150,-300]

#Solver
D = truss_analysis(coords, connect, restr, prop, load)
#print(D)

#Desenha Malha
Plot_Model(coords, connect, restr, load)
# D=np.reshape(D,(nnodes,2))
# Plot_Deformada(coords+10000*D, connect, restr, load)