import numpy as np

def k_matrix(coordsElem, propElem):
    C=np.zeros((3,3))
    C[0, :] = [1, propElem[0,1], 0]
    C[1, :] = [propElem[0,1], 1, 0]
    C[2, :] = [0, 0, (1-propElem[0,1])/2]
    C=C*(propElem[0,0]/(1-propElem[0,1]*propElem[0,1]))
    dN_rs = np.zeros((2,4))
    dN_xy = np.zeros((2,4))
    B = np.asmatrix(np.zeros((3, 8)))
    ke = np.zeros((8,8))
    #Quadratura de Gauss
    gausspoints=2
    gp, w = np.polynomial.legendre.leggauss(gausspoints)
    for i in range(gausspoints):
        r=gp[i]
        for j in range(gausspoints):
            s=gp[j]
            dN_rs[0,:] = [-(1-s)/4, (1-s)/4, (1+s)/4, -(1+s)/4]
            dN_rs[1,:] = [-(1-r)/4, -(1+r)/4, (1+r)/4, (1-r)/4]
            J = np.matmul(dN_rs,coordsElem)
            dN_xy = np.matmul(np.linalg.inv(J),dN_rs)
            B[0, :] = [dN_xy[0,0], 0, dN_xy[0,1], 0, dN_xy[0,2], 0, dN_xy[0,3], 0]
            B[1, :] = [0, dN_xy[1,0], 0, dN_xy[1,1], 0, dN_xy[1,2], 0, dN_xy[1,3]]
            B[2, :] = [dN_xy[1,0], dN_xy[0,0], dN_xy[1,1], dN_xy[0,1], dN_xy[1,2], dN_xy[0,2], dN_xy[1,3], dN_xy[0,3]]
            ke = ke + B.T* C * B * w[i] * np.linalg.det(J)

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
        node4=connect[elem,3]
        coordsElem=np.zeros((4,2))
        coordsElem[0,:]=coords[node1-1,:]
        coordsElem[1,:]=coords[node2-1,:]
        coordsElem[2,:]=coords[node3-1,:]
        coordsElem[3,:]=coords[node4-1,:]
        propElem=np.zeros((1,2))
        propElem[0,:]=prop[elem,:]
        #Element Stiffiness
        ke = k_matrix(coordsElem, propElem)
        #Assembly
        dofmap=np.zeros((1,8))
        dofmap[0,:]=[node1*2-2, node1*2-1, node2*2-2, node2*2-1, node3*2-2, node3*2-1, node4*2-2, node4*2-1]
        dofmap=dofmap.astype(int)
        for i in range(8):
            for j in range(8):
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