import numpy as np 
import scipy as sp 

# Stiffnees matrix
def stiffness(propElem,coordElem):
    E = propElem[0,0]
    A = propElem[0,1]
    x1=coordElem[0,0]
    y1=coordElem[0,1]
    x2=coordElem[1,0]
    y2=coordElem[1,1]
    le=((x2-x1)**2+(y2-y1)**2)**0.5
    c=(x2-x1)/le #cosseno
    s=(y2-y1)/le #seno
    #Matriz de transformação
    T=np.asmatrix(np.zeros((4,4)))
    T[0,0]=c
    T[0,1]=s
    T[1,0]=-s
    T[1,1]=c
    T[2,2]=c
    T[2,3]=s
    T[3,2]=-s
    T[3,3]=c
    #Matriz de rigidez no sistema local
    kl=np.asmatrix(np.zeros((4,4)))
    kl[0,0]=E*A/le
    kl[0,2]=-E*A/le
    kl[2,0]=-E*A/le
    kl[2,2]=E*A/le
    #matriz de rigidez no sistema global
    ke=np.asmatrix(np.zeros((4,4)))
    ke=T.T*kl*T
    return ke

def truss_analysis_lagrange(coords, connect, restr, prop, load):
    nelem = np.size (connect,0)
    nnodes = np.size(coords,0)
    gdl=2

    #Multiplicador de Lagrange
    count=0
    for n in range(nnodes):
        for m in range(gdl):
            if restr[n,m]== 1:
                count=count+1
    K=np.asmatrix(np.zeros((nnodes*gdl+count,nnodes*gdl+count)))
    F=np.asmatrix(np.zeros((gdl*nnodes+count,1)))
    count=0
    for n in range(nnodes):
        for m in range(gdl):
            if restr[n,m]== 1:
                count=count+1
                K[2*n+m,nnodes*gdl-1+count]=1
                K[nnodes*gdl-1+count,2*n+m]=1
                F[2*n+m+count,0]=0  

    #Assembly K
    for elem in range (nelem):
        No1=int(connect[elem,0])
        No2=int(connect[elem,1])
        coordElem=np.asmatrix(np.zeros((2,2)))
        coordElem[0,:]= coords[No1-1,:]
        coordElem[1,:]= coords[No2-1,:]
        propElem=np.asmatrix(np.zeros((1,2)))
        propElem=prop[elem,:]
        ke = stiffness(propElem, coordElem)
        #Matriz de mapeamento
        map=np.asmatrix(np.zeros((1,2*gdl)))
        map[0,0]=No1*gdl-1
        map[0,1]=No1*gdl
        map[0,2]=No2*gdl-1
        map[0,3]=No2*gdl
        for i in range(4):
            for j in range(4):
                K[int(map[0,i]-1),int(map[0,j]-1)]+=ke[i,j]

    #Assembly F
    for n in range(nnodes):
        for m in range (gdl):
            F[2*n+m,0]=load[n,m]
 
    #Solve system of equations
    # print("\n----------------------------\n")
    print("Deslocamentos e reacoes de apoio:\n")
    X=np.linalg.solve(K,F)
    print(X)

    return 0