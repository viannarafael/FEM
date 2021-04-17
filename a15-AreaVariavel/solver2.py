import numpy as np 

# Stiffnees matrix
def stiffness(propElem,coordElem):
    ke=np.asmatrix(np.zeros((2,2)))
    E= propElem[0,0]
    A0=propElem[0,2]
    Al=propElem[0,1]
    x1=coordElem[0,0]
    x2=coordElem[0,1]
    le=x2-x1
    #Quadratura de Gauss
    gausspoints=20
    gp, w = np.polynomial.legendre.leggauss(gausspoints)
    for i in range(gausspoints):
        r = (gp[i]+1)*le/2  # Mudanca de intervalo de integracao de -1 e 1 pra 0 e L
        Ar = A0+ r*(Al-A0)/le
        dAdr = (Al-A0)/le
        dN1dr= dAdr*(1/Ar)*(1/(np.log(A0)-np.log(Al)))
        dN2dr= -dN1dr
        detJ=le/2 
        B=np.asmatrix(np.zeros((1,2)))
        B[0,0]=dN1dr
        B[0,1]=dN2dr
        ke = ke + B.T* E * B * Ar  * w[i] * detJ
    return ke

def solve_ln(coords, connect, restr, prop, load):
    nelem = np.size (connect,0)
    nnodes = np.size(coords,0)
    #Assembly - Matriz de Incidencia
    K=np.asmatrix(np.zeros((nnodes,nnodes)))
    for elem in range (nelem):
        coordElem=np.asmatrix(np.zeros((1,2)))
        coordElem[0,0]= coords[elem]
        coordElem[0,1]= coords[elem+1]
        propElem=np.asmatrix(np.zeros((1,3)))
        propElem=prop[elem,:]
        ke = stiffness(propElem, coordElem)
        #Matriz de Incidencia
        T=np.asmatrix(np.zeros((2,nnodes)))
        for i in range(2):
            T[i,int(connect[elem,i])] = 1
        K = K + T.T*ke*T
    
    #Condensed Matrix
    Kr=np.asmatrix(np.zeros((nelem,nelem)))
    Fr=np.asmatrix(np.zeros((nelem,1)))
    for i in range(nelem):
        Fr [i,0]= load[i+1,0]
        for j in range(nelem):
            Kr [i,j]= K[i+1,j+1]

    #Solve linear system
    D = np.linalg.solve(Kr,Fr)
    print(K)
    print(load)

    #Nodal displacement
    Dnew = np.asmatrix(np.zeros((nelem+1,1)))
    for i in range(nelem):
        Dnew [i+1,0]= D[i,0]
    return(Dnew)
    

