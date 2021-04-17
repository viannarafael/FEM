import numpy as np
from solver import solve_linear
from solver2 import solve_ln
from matplotlib import pyplot as plt

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
E = 205.0               #Young`s modulus
L = 2.0                 #bar length
c = 10.0                #load
h0 = 0.6                #initial hight
hl = 0.2                #final hight
t = 0.05                #thickness
gama = 77               #density
total_iterations=10     #number of iterations

x=np.asmatrix(np.zeros((total_iterations,1)))
y_linear=np.asmatrix(np.zeros((total_iterations,1)))
y_ln=np.asmatrix(np.zeros((total_iterations,1)))
for iteration in range(total_iterations):  
    nbars=iteration+1   #number of bars
    nnodes = nbars+1    #number of nodes    

    #Matriz de coordenadas
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
    prop2=np.asmatrix(np.zeros((nbars,3)))
    for elem in range (nbars):
        prop[elem,0] = E
        prop2[elem,0] = E
        b1=hl+(h0-hl)*(L-elem*L/nbars)/L
        b2=hl+(h0-hl)*(L-(elem+1)*L/nbars)/L
        prop[elem,1] = (b1+b2)/2*t
        prop2[elem,1] = b2*t
        prop2[elem,2] = b1*t

    #Vetor de Cargas
    load=np.asmatrix(np.zeros((nbars+1,1)))
    for elem in range(nbars):
        b1=hl+(h0-hl)*(L-elem*L/nbars)/L
        b2=hl+(h0-hl)*(L-(elem+1)*L/nbars)/L
        P=gama*t*(b1+b2)/2*L/nbars
        load[elem,0]=load[elem,0]+P/2
        load[elem+1,0]=load[elem+1,0]+P/2
        # f=equivalentload(b1*t*gama,b2*t*gama,L/nbars)
        # load[elem,0]=load[elem,0]+f[0,0]
        # load[elem+1,0]=load[elem+1,0]+f[1,0]

    # print("coords =\n",coords)
    # print("\nconnect =\n",connect)
    # print("\nload =\n",load)
    # print("\nrestr =\n",restr)
    # print("\nprop =\n",prop)

    D_linear = solve_linear(coords, connect, restr, prop, load)
    D_ln = solve_ln(coords, connect, restr, prop2, load)
    
    x[iteration]=nbars
    y_linear[iteration]=D_linear[nbars]
    y_ln[iteration]=D_ln[nbars]

plt.plot(x, y_linear,y_ln)
plt.title('Convergence of Bar under Axial Force')
plt.xlabel('Number of elements')
plt.ylabel('Displacement of the last node')
plt.legend(['Linear interpolation','Ln interpolation'])
plt.show()
