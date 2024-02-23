from pythonds.graphs import PriorityQueue

from utils import myGraph, Vertex, createGraph

def Dijkstra(aGraph:myGraph, start:Vertex):
    """single-source shortest path problem solver, using Dijkstra algorithm"""

    for vert in aGraph:
        vert.dist = float('inf') # 重置一下各点的distance，这样多次执行该函数的时候才不会出错
        vert.pred = None # 重置一下各节点的前驱

    start.setDistance(0)

    pq = PriorityQueue()
    pq.buildHeap([(v.getDistance(),v) for v in aGraph])

    while not pq.isEmpty():
        currentVert:Vertex = pq.delMin()
        for nextVert in currentVert.getConnections():
            newDist = currentVert.getDistance() + currentVert.getWeight(nextVert)
            if newDist < nextVert.getDistance():
                nextVert.setDistance(newDist) # 不是很确定能否这样声明类型Vertex
                nextVert.setPred(currentVert)
                pq.decreaseKey(nextVert,newDist)
    return aGraph

def oneToAllShortestPath(G:myGraph, startName:str):
    """Given one location, show the shortest paths from all locations on the
    map to this one and their length, using Dijkstra algorithm"""
    # g = createGraph() # 读取助教提供的edge.txt文件，并转换成myGraph实例
    # start = g.getVertex(startName)
    start = G.getVertex(startName)
    g = Dijkstra(G,start) # 计算所有点到起点start的距离
    loc_path_dist = []
    
    for terminalName in g.getVertices():
        terminal = g.getVertex(terminalName)
        path, dist = g.shortestPathTo(terminal)
        loc_path_dist.append( (terminalName, path, dist) )
    
    return loc_path_dist


# def busRoutes(G:myGraph,startName:str):
#     """
#     Given one location, such as A, you need to provide the path and
#     distance for designing bus routes starting from A, and ensure that the bus
#     route is the shortest. In addition:
#     a. The shortest path from all other points to A through this bus route
#     remains the same length as before.
#     b. Any two points can be reached through the designed bus route.
#     """
#     loc_path_dist = oneToAllShortestPath(G,startName)



def main():
    g = createGraph()
    while True:
        start = input('请输入起点：')
        if start not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ':
            continue
        else:
            loc_path_dist = oneToAllShortestPath(g,start)
            for item in loc_path_dist:
                terminal, path, dist = item 
                print('terminal is: ',terminal)
                print('path is: ')
                for v in path:
                    print(v,'-->',end='')

                print('\ndistance is: ',dist)
                print()

if __name__ == '__main__':
    main()


