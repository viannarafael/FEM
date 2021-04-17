import numpy as np  

# Stiffnees matrix
def stiffness(propElem,coordElem):
    E = propElem[0,0]
    A = propElem[0,1]
    I = propElem[0,2]
    x1=coordElem[0,0]
    y1=coordElem[0,1]
    x2=coordElem[1,0]
    y2=coordElem[1,1]
    # [x1,y1]=coordElem[0,:]
    # [x2,y2]=coordElem[1,:]
    le=((x2-x1)**2+(y2-y1)**2)**0.5
    c=(x2-x1)/le #cosseno
    s=(y2-y1)/le #seno
    #Matriz de transformação
    T=np.asmatrix(np.zeros((6,6)))
    T[0,0]=c
    T[0,1]=s
    T[1,0]=-s
    T[1,1]=c
    T[2,2]=1
    T[3,3]=c
    T[3,4]=s
    T[4,3]=-s
    T[4,4]=c
    T[5,5]=1
    #Matriz de rigidez no sistema local
    kl=np.asmatrix(np.zeros((6,6)))
    kl[0,0]=E*A/le
    kl[0,3]=-E*A/le
    kl[1,1]=GAq/le    
    kl[1,2]=-GAq/2
    kl[1,4]=-GAq/le
    kl[1,5]=-GAq/2
    kl[2,1]=-GAq/2
    kl[2,2]=GAq*le/3+EI/le
    kl[2,4]=GAq/2
    kl[2,5]=GAq*le/6-EI/le
    kl[3,0]=-E*A/le
    kl[3,3]=E*A/le
    kl[4,1]=-GAq/le
    kl[4,2]=GAq/2
    kl[4,4]=GAq/le
    kl[4,5]=GAq/2
    kl[5,1]=-GAq/2
    kl[5,2]=GAq*le/6-EI/le
    kl[5,4]=GAq/2
    kl[5,5]=GAq*le/3+E*I/le
    #matriz de rigidez no sistema global
    ke=np.asmatrix(np.zeros((6,6)))
    ke=T.T*kl*T
    return ke

def solver_bernoulli (coords, connect, prop, elem, load)
    nelems=np.size(connect)
    nnodes=np.size(coords)
    gdl=2
    for ele in range (nelem)
        No1=int(connect[elem,0]-1)
        No2=int(connect[elem,1]-1)
        coordElem=np.asmatrix(np.zeros((2,2)))
        coordElem[0,:]= coords[No1-1,:]
        coordElem[1,:]= coords[No2-1,:]
        propElem=np.asmatrix(np.zeros((1,3)))
        propElem=prop[elem,:]
        ke = stiffness(propElem, coordElem)
        map=[[No1*3-2 No1*3-1 No1*3 No2*3-2 No2*3-1 No2*3]]
        for i in range(6):
            for j in range(6):
                K[int(map[0,i]-1),int(map[0,j]-1)]=K[int(map[0,i]-1),int(map[0,i]-1)]+ke[i,j]
    #Penalty method
    restr=np.reshape(restr,(nnodes*gdl,1))
    F=np.reshape(load,(nnodes*gdl,1))
    #print(F)
    for i in range (nnodes*gdl):
       if restr[i,0]==1:
           K[i,i]=10e20
    #Solve linear system
    D = np.linalg.solve(K,F)
    return(D)