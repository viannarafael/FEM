import numpy as np 

# Stiffnees matrix
def stiffness(propElem,coordElem):
    E = propElem[0,0]
    A = propElem[0,1]
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

def truss_analysis(coords, connect, restr, prop, load):
    nelem = np.size (connect,0)
    nnodes = np.size(coords,0)
    gdl=2

    #Ordenação dos graus de Liberdade
    count=0
    ID_GDL=np.asmatrix(np.zeros((nnodes,gdl)))
    for n in range(nnodes):
        for m in range(gdl):
            if restr[n,m]== 0:
                count=count+1
                ID_GDL[n,m]=count 
    gdllivre=count
    for n in range(nnodes):
        for m in range(gdl):
            if restr[n,m]== 1:
                count=count+1
                ID_GDL[n,m]=count 
    gdlfixo=count-gdllivre

    #Assembly - Matriz de Incidencia
    K=np.asmatrix(np.zeros((nnodes*gdl,nnodes*gdl)))
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
        map[0,0]=ID_GDL[No1-1,0]
        map[0,1]=ID_GDL[No1-1,1]
        map[0,2]=ID_GDL[No2-1,0]
        map[0,3]=ID_GDL[No2-1,1]
        for i in range(4):
            for j in range(4):
                K[int(map[0,i]-1),int(map[0,j]-1)]+=ke[i,j]

    #Condensed Matrix
    KLL=np.asmatrix(np.zeros((gdllivre,gdllivre)))
    FL=np.asmatrix(np.zeros((gdllivre,1)))
    DL=np.asmatrix(np.zeros((gdllivre,1)))
    F=np.asmatrix(np.zeros((gdl*nnodes,1)))
    for n in range(nnodes):
        for m in range (gdl):
            F[int(ID_GDL[n,m]-1),0]=load[n,m]

    for i in range(gdllivre):
        for j in range(gdllivre):
            KLL[i,j]=K[i,j]
            FL[i,0]=F[i,0]
    
    DL = np.linalg.solve(KLL,FL)
    D = np.asmatrix(np.zeros((gdl*nnodes,1)))
    for i in range(gdllivre):
        D[i,0]=DL[i,0]

    #Reações de Apoio
    print("\n----------------------------\n")
    print("Reações de Apoio:\n")
    KFL = np.asmatrix(np.zeros((gdlfixo,gdllivre)))
    for i in range(gdlfixo):
        for j in range(gdllivre):
            KFL[i,j]=K[gdllivre+i,j]
    R=np.matmul(KFL,DL)
    print(R)

    #Esforço interno
    print("\n----------------------------\n")
    print("Esforços Internos:\n")
    for elem in range (nelem):
        No1=int(connect[elem,0])
        No2=int(connect[elem,1])
        E = prop[elem,0]
        A = prop[elem,1]
        x1=coords[No1-1,0]
        y1=coords[No1-1,1]
        x2=coords[No2-1,0]
        y2=coords[No2-1,1]
        le=((x2-x1)**2+(y2-y1)**2)**0.5
        c=(x2-x1)/le #cosseno
        s=(y2-y1)/le #seno
        #Deslocamento no sistema global
        dg=np.asmatrix(np.zeros((1,2*gdl)))
        dg[0,0]=D[int(ID_GDL[No1-1,0]-1)]  
        dg[0,1]=D[int(ID_GDL[No1-1,1]-1)]
        dg[0,2]=D[int(ID_GDL[No2-1,0]-1)]
        dg[0,3]=D[int(ID_GDL[No2-1,1]-1)]
        #Mudança pro sistema local
        T=np.asmatrix(np.zeros((4,4)))
        T[0,0]=c
        T[0,1]=s
        T[1,0]=-s
        T[1,1]=c
        T[2,2]=c
        T[2,3]=s
        T[3,2]=-s
        T[3,3]=c
        dl=T*dg.T
        # Deformação
        B=np.asmatrix(np.zeros((2,4)))
        B[0,0]=-1/le
        B[0,2]=1/le
        B[1,1]=-1/le
        B[1,3]=1/le
        Nl=np.asmatrix(np.zeros((2,1)))
        Nl = E*B*dl*A
        # Mudança pro sistema global
        print("Barra", elem+1,": ", "N = ",-Nl[0,0])

    return(D)