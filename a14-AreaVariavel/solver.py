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
    w=np.asmatrix(np.zeros((1,1)))
    w[0,0]=2
    #w[0,1]=1
    gp=np.asmatrix(np.zeros((1,1)))
    gp[0,0]=0
    #gp[0,1]=1/(np.sqrt(3))

    for i in range(1):
        r = gp [0,i]
        dN1dr=-1/le
        dN2dr=1/le
        #Jinv=np.asmatrix(np.zeros((1,2)))
        #Jinv[0,0]=dN1dr*x1
        #Jinv[0,1]=dN2dr*x2
        #J=np.linalg.inv(Jinv)
        detJ=le*0.5
        #detJ=np.linalg.det(Jinv)
        B=np.asmatrix(np.zeros((1,2)))
        B[0,0]=dN1dr
        B[0,1]=dN2dr
        ke = ke + B.T* E * A * B * detJ * w[0,i]
    
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
    

