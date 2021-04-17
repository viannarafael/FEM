import matplotlib.pyplot as plt
import numpy as np

# ------------------------
# Plotagem do modelo
def Plot_Model(coords, connect, restr, load):
    nnodes=np.size(coords,0)
    nelem=np.size(connect,0)
    fig=plt.figure() #criando figura
    ax = fig.add_subplot(111) #criação do subplot
    
    # ------------------------
    #Plot elemento por elemento
    x=np.asmatrix(np.zeros((2,1))) #inicializa as coordenadas dos nós de cada elemento
    y=np.asmatrix(np.zeros((2,1)))
    for elem in range (nelem):
        No1=int(connect[elem,0])-1
        No2=int(connect[elem,1])-1
        x= [coords[No1,0], coords[No2,0]]
        y= [coords[No1,1], coords[No2,1]]
        ax=plt.plot(x,y,marker="o",color='b')
        
    # ------------------------
    #Plot condicao de contorno
    for n in range (nnodes):
        #Cargas
        if (load[n,0]!=0):
            x=coords[n,0]
            y=coords[n,1]
            dx=1*((load[n,0]>0))-1*((load[n,0]<0))
            ax=plt.arrow(x,y,dx,0, facecolor='r', edgecolor='r', width=0.005,head_width=0.1)
        if (load[n,1]!=0):
            x=coords[n,0]
            y=coords[n,1]
            dy=1*((load[n,1]>0))-1*((load[n,1]<0))
            ax=plt.arrow(x,y,0,dy, facecolor='r', edgecolor='r', width=0.005,head_width=0.1)
        #Apoios
        if (restr[n,0]==1):
            x=coords[n,0]-0.1
            y=coords[n,1]
            ax=plt.scatter(x,y, s=150, marker='>', color='m')
        if (restr[n,1]==1):
            x=coords[n,0]
            y=coords[n,1]-0.1
            ax=plt.scatter(x,y, s=150, marker='^', color='m')  

    # ------------------------
    
    plt.show()


# ------------------------
# Plotagem da deformada
def Plot_Deformada(coords, connect, restr, load):
    nnodes=np.size(coords,0)
    nelem=np.size(connect,0)
    fig=plt.gcf() #criando figura
    #ax1=plt.gca() #criando figura
    ax = fig.add_subplot(111) #criação do subplot
    # ------------------------
    #Plot elemento por elemento
    x=np.asmatrix(np.zeros((2,1))) #inicializa as coordenadas dos nós de cada elemento
    y=np.asmatrix(np.zeros((2,1)))
    for elem in range (nelem):
        No1=int(connect[elem,0])-1
        No2=int(connect[elem,1])-1
        x= [coords[No1,0], coords[No2,0]]
        y= [coords[No1,1], coords[No2,1]]
        ax=plt.plot(x,y,marker=".",color='r', linestyle='--')
       
    # ------------------------
    plt.show()


    