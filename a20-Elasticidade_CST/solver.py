import numpy as np

def k_matrix(coordsElem, propElem):
    [x1, y1]=coordsElem[0,:]
    [x2, y2]=coordsElem[1,:]
    [x3, y3]=coordsElem[2,:]
    C=np.zeros((3,3))
    C[0, :] = [1, propElem[0,1], 0]
    C[1, :] = [propElem[0,1], 1, 0]
    C[2, :] = [0, 0, (1-propElem[0,1])/2]
    C=C*(propElem[0,0]/(1-propElem[0,1]*propElem[0,1]))
    A=((x2*y3-x3*y2)-(x1*y3-x3*y1)+(x1*y2-x2*y1))/2
    B = np.asmatrix(np.zeros((3, 6)))
    B[0, :] = [(y2-y3), 0, (y3-y1), 0, (y1-y2), 0]
    B[1, :] = [0, (x3-x2), 0, (x1-x3), 0, (x2-x1)]
    B[2, :] = [(x3-x2),(y2-y3),(x1-x3),(y3-y1),(x2-x1),(y1-y2)]
    B=B/(2*A)
    ke = B.T*C*B*A
    return ke

def solver(coords, connect, load, restr, prop):
    numElems=np.size(connect,0)
    numNodes=np.size(coords,0)
    gdl=2
    K=np.zeros((numNodes*gdl,numNodes*gdl))
    F=np.zeros((numNodes*gdl,1))
    D=np.zeros((numNodes*gdl,1))
    for elem in range(numElems):
        node1=connect[elem,0]
        node2=connect[elem,1]
        node3=connect[elem,2]
        coordsElem=np.zeros((3,2))
        coordsElem[0,:]=coords[node1-1,:]
        coordsElem[1,:]=coords[node2-1,:]
        coordsElem[2,:]=coords[node3-1,:]
        propElem=np.zeros((1,2))
        propElem[0,:]=prop[elem,:]
        #Element Stiffiness
        ke = k_matrix(coordsElem, propElem)
        #Assembly
        dofmap=np.zeros((1,6))
        dofmap[0,:]=[node1*2-2, node1*2-1, node2*2-2, node2*2-1, node3*2-2, node3*2-1]
        dofmap=dofmap.astype(int)
        for i in range(6):
            for j in range(6):
                K[dofmap[0,i],dofmap[0,j]]+=ke[i,j]
    F=load.reshape(numNodes*gdl,1)
    # Apply constrain and solve
    nullNode=sum(np.where(restr.reshape(numNodes*gdl,1)==1)).astype(int)
    Kll=np.delete(np.delete(K,np.unique(nullNode[:]),0),np.unique(nullNode[:]),1)
    Fl=np.delete(F,np.unique(nullNode[:]),0)
    Dl=np.linalg.solve(Kll,Fl)
    #Compute D
    i=0
    for n in range(numNodes*gdl):
        if (n not in np.unique(nullNode[:])):
            D[n]=Dl[i]
            i=i+1
    print("\nD=",D)
    return D