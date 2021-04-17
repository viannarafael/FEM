import matplotlib.pyplot as plt

def viewmesh(coords, connect, loads, restrs):
    color = 'cornflowerblue'
    linestyle = '-'
    bbox = {'fc': '0.8', 'pad': 2}
    props = {'ha': 'left', 'va': 'bottom', 'bbox': bbox}
    dr = 0.05
    dl = 0.5/max(max(loads[:,0]),max(loads[:,1])) 
    ds = 0.15
    minX = min(coords[:,0])  
    minY = min(coords[:,1])  
    maxX = max(coords[:,0])  
    maxY = max(coords[:,1])  
    delta = max(maxX-minX,maxY-minY)
    dr *= delta
    w, h = plt.figaspect(coords)
    fig = plt.figure(figsize=(w, h))  
    ax = fig.add_subplot(111)
    ratio = 1.0
    xleft, xright = ax.get_xlim()
    ybottom, ytop = ax.get_ylim()
    ax.set_aspect(abs((xright-xleft)/(ybottom-ytop))*ratio)
    ax.axis([minX-delta*ds,maxX+delta*ds,minY-delta*ds,maxY+delta*ds])

    count = 1
    for e in connect:
        x = []
        y = []
        xm = 0
        ym = 0
        for n in range(e[0]):
            x.append(coords[e[n+1]-1,0])
            y.append(coords[e[n+1]-1,1])
            xm += coords[e[n+1]-1,0]
            ym += coords[e[n+1]-1,1]
        ax.text(xm/e[0], ym/e[0],str(count),props, rotation = 0)
        count += 1
        ax.plot(x, y, linestyle=linestyle, color=color, linewidth=3)
    color = 'black'
    ax.plot(coords[:,0], coords[:,1],'o', color=color)

    count = 1
    for n in coords:
        ax.text(n[0]+0.1, n[1]+0.1,str(count), color='black')
        ax.arrow(n[0],n[1],loads[count-1,0]*dl, loads[count-1,1]*dl,width=dl/2.0, head_width=dl*2.0, head_length=dl*2.0,length_includes_head=True, color='red')
        if restrs[count-1, 0] == 1:
            ax.plot([n[0] - dr, n[0] - dr], [n[1] - dr/2.0, n[1]  + dr/2.0], color='green')
            ax.plot([n[0] - dr, n[0]], [n[1]  - dr/2.0, n[1] ], color='green')
            ax.plot([n[0] - dr, n[0]], [n[1]  + dr/2.0, n[1] ], color='green')
        if restrs[count-1, 1] == 1:
            ax.plot([n[0] - dr/2.0, n[0] +dr/2.0], [n[1] - dr, n[1]  - dr], color='green')
            ax.plot([n[0] - dr/2.0, n[0]], [n[1]  - dr, n[1] ], color='green')
            ax.plot([n[0] , n[0]+dr/2.0], [n[1]  , n[1] -dr], color='green')

        count += 1

    plt.xlabel('x - axis')   
    plt.ylabel('y - axis')
    plt.show()

"""
                if restraint_x_axis != 0:
                    plt.plot([x_coordinate - 0.1, x_coordinate - 0.1], [y_coordinate - 0.05, y_coordinate + 0.05],
                             color='black')
                    plt.plot([x_coordinate - 0.1, x_coordinate], [y_coordinate - 0.05, y_coordinate], color='black')
                    plt.plot([x_coordinate - 0.1, x_coordinate], [y_coordinate + 0.05, y_coordinate], color='black')

                if restraint_y_axis != 0:
                    plt.plot([x_coordinate - 0.05, x_coordinate + 0.05], [y_coordinate - 0.1, y_coordinate - 0.1],
                             color='black')
                    plt.plot([x_coordinate - 0.05, x_coordinate], [y_coordinate - 0.1, y_coordinate], color='black')
                    plt.plot([x_coordinate, x_coordinate + 0.05], [y_coordinate, y_coordinate - 0.1], color='black')
"""                    