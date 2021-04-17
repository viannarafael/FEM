import numpy as np
from matplotlib import pyplot as plt
from solver import *
from solver_ordenado import *
from desenhamalha import *

#Input 
E = 210e6         #Young`s modulus
A = 5*10e-3            #Cross sectional area
nnodes= 3
nelem=2

#Matriz de coordenadas
coords=np.asmatrix(np.zeros((nnodes,2)))
coords[0,:]= [5,5]
coords[1,:]= [0,0]
coords[2,:]= [5,0]

#Matriz de conectividade
connect=np.asmatrix(np.zeros((nelem,2)))
connect[0,:]=[2,1]
connect[1,:]=[1,3]

# Matriz de restricoes
restr=np.asmatrix(np.zeros((nnodes,2)))
restr[1,:]=[1,1]
restr[2,:]=[1,1]

#Matriz de Propriedades
prop=np.asmatrix(np.zeros((nelem,2)))
for elem in range (nelem):
    prop[elem,:] = [E,A]

#Vetor de Cargas
load=np.asmatrix(np.zeros((nnodes,2)))
load[0,:]=[10,0]

#Solver
print("\n*****************************************************\n")
print("Metodo de Multiplicadores de Lagrange:\n")
D = truss_analysis_lagrange(coords, connect, restr, prop, load)
print("\n*****************************************************\n")
print("Metodo de Mapeamento:\n")
D = truss_analysis_ordenado(coords, connect, restr, prop, load)
#print(D)

#Desenha Malha
Plot_Model(coords, connect, restr, load)
