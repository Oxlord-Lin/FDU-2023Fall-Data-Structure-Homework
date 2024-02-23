"""
provide the path and distance for designing the subway
routes based on the current road, which needs to meet these conditions:
a. All locations are included in this route.
b. The selected route has the shortest distance among all possible routes.

Using prim algorithm to find the minimum spanning tree
"""

from pythonds.graphs import PriorityQueue
from utils import myGraph, Vertex, createGraph

def prim(G:myGraph,startName:str):
    """Prim算法，也称加点法，基于贪心策略，利用优先队列，把距离“最近”的点依次加入最小生成树"""
    pq = PriorityQueue()
    for v in G: # 初始化
        v.setDistance(float('inf')) # 所有的距离都设置为最大
        v.setPred(None) # 所有节点的前驱都清空
    
    start = G.getVertex(startName)
    start.setDistance(0)
    pq.buildHeap([(v.getDistance(),v) for v in G])

    while not pq.isEmpty():
        currentVert :Vertex= pq.delMin()
        for nextVert in currentVert.getConnections():
            w = currentVert.getWeight(nextVert)
            if nextVert in pq and w < nextVert.getDistance(): # 一端是生成树中的顶点，另一端是还不在生成树中的顶点
                nextVert.setPred(currentVert)
                nextVert.setDistance(w)
                pq.decreaseKey(nextVert,w)

    return G.showMinimumSpanningTree(start)

def main():
    g = createGraph()
    edges, distance = prim(g,'F')
    print(edges)
    print('距离为：',distance)

if __name__ == '__main__':
    main()




        
