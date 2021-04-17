import numpy as np 

# Stiffnees matrix
def stiffness(E, A, L):
    k=np.asmatrix(np.zeros((2,2)))
    k[0,0]=E*A/L
    k[0,1]=-E*A/L
    k[1,0]=-E*A/L
    k[1,1]=E*A/L
    return k

def solve(coords, connect, restr, prop, load):

    nelem = np.size (connect,0)
    nnodes = np.size(coords,0)
    le = coords[1]-coords[0]
    ke = stiffness(prop[0,0], prop[0,1], le)
    
    #Assembly - Matriz de Incidencia
    K=np.asmatrix(np.zeros((nnodes,nnodes)))
    for elem in range (nelem):
        T=np.asmatrix(np.zeros((2,nnodes)))
        for i in range(2):
            T[i,int(connect[elem,i])] = 1
        #print("Elem=",elem, "\nT=\n",T) 
        K = K + T.T*ke*T
        #print(K)

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
    print("For",nelem, "bars,\n\n D= \n")
    print(Dnew)
        