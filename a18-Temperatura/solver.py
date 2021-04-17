import numpy as np

def k_matrix(coordsElem, propElem):
    [x1, y1]=coordsElem[0,:]
    [x2, y2]=coordsElem[1,:]
    [x3, y3]=coordsElem[2,:]
    A=((x2*y3-x3*y2)-(x1*y3-x3*y1)+(x1*y2-x2*y1))/2
    B = np.asmatrix(np.zeros((2, 3)))
    B[0, :] = [(y2-y3), (y3-y1), (y1-y2)]
    B[1, :] = [(x3-x2), (x1-x3), (x2-x1)]
    B=B/(2*A)
    ke = B.T*B*propElem[0,0]*A
    return ke

def source(coordsElem, propElem, bcElem):
    [x1, y1]=coordsElem[0,:]
    [x2, y2]=coordsElem[1,:]
    [x3, y3]=coordsElem[2,:]
    A=((x2*y3-x3*y2)-(x1*y3-x3*y1)+(x1*y2-x2*y1))/2
    B=np.zeros((2,3))
    B[0, :] = [(y2-y3), (y3-y1), (y1-y2)]
    B[1, :] = [(x3-x2), (x1-x3), (x2-x1)]
    B=B/(2*A)
    J = np.matmul(B,coordsElem)
    s = propElem[0,1]
    fs=np.zeros((3,1))
    fs[:,0] = s*A/3
    return fs

def q_vector(coordsElem, edgesElem, flux):
    X=np.zeros((3,2))
    X[0,:]=coordsElem[0,:]
    X[1,:]=coordsElem[1,:]
    X[2,:]=coordsElem[2,:]
    [x1, y1]=X[0,:]
    [x2, y2]=X[1,:]
    [x3, y3]=X[2,:]
    A=((x2*y3-x3*y2)-(x1*y3-x3*y1)+(x1*y2-x2*y1))/2
    fq=np.zeros((3,1))
    for ed in range(3):
        if (flux[int(edgesElem[0,ed])-1,0]==1):
            q=flux[int(edgesElem[0,ed])-1,1]
            n1=ed
            n2=n1+1
            if (n2==3):
                n2=0
            if (X[int(n1),1]-X[int(n2),1]==0):
                # print("Paralelo a X")
                y=X[int(n1),1]
                l=X[int(n1),0]-X[int(n2),0]
                detJ=l*0.5
                gausspoints=2
                gp, w = np.polynomial.legendre.leggauss(gausspoints)
                for i in range(gausspoints):
                    r=(gp[i]+1)*l*0.5
                    wr=w[i]  
                    N=np.zeros((1,3))    
                    N[0,0]=(x2*y3-x3*y2+(y2-y3)*r+(x3-x2)*y)/(2*A)
                    N[0,1]=(x3*y1-x1*y3+(y3-y1)*r+(x1-x3)*y)/(2*A)
                    N[0,2]=(x1*y2-x2*y1+(y1-y2)*r+(x2-x1)*y)/(2*A)
                    fq += -N.T*q*wr*detJ
            if (X[int(n1),0]-X[int(n2),0]==0):
                # print("Paralelo a Y")
                x=X[int(n1),0]
                l=X[int(n1),1]-X[int(n2),1]
                detJ=0.5*l
                gausspoints=2
                gp, w = np.polynomial.legendre.leggauss(gausspoints)
                for i in range(gausspoints):
                    r=(gp[i]+1)*l*0.5
                    wr=w[i]      
                    N=np.zeros((1,3))    
                    N[0,0]=(x2*y3-x3*y2+(y2-y3)*x+(x3-x2)*r)/(2*A)
                    N[0,1]=(x3*y1-x1*y3+(y3-y1)*x+(x1-x3)*r)/(2*A)
                    N[0,2]=(x1*y2-x2*y1+(y1-y2)*x+(x2-x1)*r)/(2*A)
                    fq += -N.T*q*wr*detJ
    return fq

def solver(coords, connectEdges, edgesElem, connect, temp, flux, prop):
    numElems=np.size(connect,0)
    numEdges=np.size(connectEdges,0)
    numNodes=np.size(coords,0)
    K=np.zeros((numNodes,numNodes))
    F=np.zeros((numNodes,1))
    T=np.zeros((numNodes,1))
    for elem in range(numElems):
        #print("elem=",elem)
        edge=np.zeros((1,3))
        edge1=edgesElem[elem,0]
        edge2=edgesElem[elem,1]
        edge3=edgesElem[elem,2]
        edges=np.zeros((1,3))
        edges[0,:]=[edge1, edge2, edge3]
        #print("edgesElem=",edges)
        node1=connect[elem,0]
        node2=connect[elem,1]
        node3=connect[elem,2]
        #print("nodes=",node1, node2, node3)
        coordsElem=np.zeros((3,2))
        coordsElem[0,:]=coords[node1-1,:]
        coordsElem[1,:]=coords[node2-1,:]
        coordsElem[2,:]=coords[node3-1,:]
        #print("coordsElem=",coordsElem)
        propElem=np.zeros((1,2))
        propElem[0,:]=prop[elem,:]
        #Call functions
        ke = k_matrix(coordsElem, propElem)
        fs = source(coordsElem, propElem, 0)
        fq= q_vector(coordsElem, edges, flux)
        fe=fs+fq
        #Assembly
        dofmap=np.zeros((1,3))
        dofmap[0,:]=[node1-1, node2-1, node3-1]
        dofmap=dofmap.astype(int)
        for i in range(3):
            for j in range(3):
                K[dofmap[0,i],dofmap[0,j]]+=ke[i,j]
            F[dofmap[0,i]]+=fe[i]

    # Apply constrain and solve
    r=sum(np.where(temp[:,0]==1)).astype(int)
    nullNode=np.zeros((2*np.size(r,0)))
    for i in range(np.size(r,0)):
        for j in range(2):
            nullNode[2*i+j]=connectEdges[int(r[i]),j]-1
    Kll=np.delete(np.delete(K,np.unique(nullNode[:]),0),np.unique(nullNode[:]),1)
    Fl=np.delete(F,np.unique(nullNode[:]),0)
    Tl=np.linalg.solve(Kll,Fl)
    
    #Compute T
    i=0
    for n in range(numNodes):
        if (n not in np.unique(nullNode[:])):
            T[n]=Tl[i]
            i=i+1

    print("\nT=",T)
    return T