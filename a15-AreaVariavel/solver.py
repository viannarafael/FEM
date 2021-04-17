import numpy as np 

# Stiffnees matrix
def stiffness(propElem,coordElem):
    ke=np.asmatrix(np.zeros((2,2)))
    E= propElem[0,0]
    A=propElem[0,1]
    x1=coordElem[0,0]
    x2=coordElem[0,1]
    le=x2-x1
    
    #Quadratura de Gauss
    gausspoints=1
    gp, w = np.polynomial.legendre.leggauss(gausspoints)
    for i in range(1):
        dN1dr=-1/le
        dN2dr=1/le
        detJ=le*0.5
        B=np.asmatrix(np.zeros((1,2)))
        B[0,0]=dN1dr
        B[0,1]=dN2dr
        ke = ke + B.T* E * A * B * w[i] * detJ
    
    return ke

def solve_linear(coords, connect, restr, prop, load):
    nelem = np.size (connect,0)
    nnodes = np.size(coords,0)
    
    #Assembly - Matriz de Incidencia
    K=np.asmatrix(np.zeros((nnodes,nnodes)))
    for elem in range (nelem):
        coordElem=np.asmatrix(np.zeros((1,2)))
        coordElem[0,0]= coords[elem]
        coordElem[0,1]= coords[elem+1]
        propElem=np.asmatrix(np.zeros((1,2)))
        propElem=prop[elem,:]
        ke = stiffness(propElem, coordElem)
        #Matriz de Incidencia
        T=np.asmatrix(np.zeros((2,nnodes)))
        for i in range(2):
            T[i,int(connect[elem,i])] = 1
        K = K + T.T*ke*T

    # #Penalty method
    # for i in range (nnodes):
    #    if restr[i]==True:
    #        K[i,i]=10e20
    # #Solve linear system
    # D = np.linalg.solve(K,load)
    # print("For",nelem, "bars,\n\n D= \n")
    # print(D)

    #Reduced Matrix
    Kr=np.asmatrix(np.zeros((nelem,nelem)))
    Fr=np.asmatrix(np.zeros((nelem,1)))
    for i in range(nelem):
        Fr [i,0]= load[i+1,0]
        for j in range(nelem):
            Kr [i,j]= K[i+1,j+1]

    #Solve linear system
    D = np.linalg.solve(Kr,Fr)

    #Print nodal displacement
    Dnew = np.asmatrix(np.zeros((nelem+1,1)))
    for i in range(nelem):
        Dnew [i+1,0]= D[i,0]
        
    return(Dnew)
    

