from utils import myGraph,Vertex,createGraph
# from pythonds.graphs import Vertex
from Dijkstra import oneToAllShortestPath
import numpy as np
import pandas as pd


def Bellman_Ford(G:myGraph, start:Vertex):
    """单源最短路径，基于Bellman-Ford算法实现，给定start节点，
    计算其他节点到该节点的最短路径和最短路径长度"""
    neg_cycle = False
    for v in G:
        v.setDistance(float('inf')) # 重置每个节点的到起点的距离，防止反复调用该函数的时候出错
        v.setPred(None) # 重置每个节点的前驱，防止多次调用该函数的时候出错

    start.setDistance(0)

    n = len(G.getVertices()) # 节点个数
    edges = G.getEdges() # 所有的边，以默认字典存储

    for _ in range(n-1): # 做n-1轮
        for e in list(edges.keys()):
            u,v = e
            u_Vert :Vertex = G.getVertex(u)
            v_Vert :Vertex = G.getVertex(v)
            if v_Vert.getDistance() > u_Vert.getDistance() + edges[(u,v)]:
                v_Vert.setDistance(u_Vert.getDistance() + edges[(u,v)])
                v_Vert.setPred(u_Vert)

    # 第n轮检查是否存在负环
    for e in list(edges.keys()):
        u,v = e
        u_Vert :Vertex = G.getVertex(u)
        v_Vert :Vertex = G.getVertex(v)
        if v_Vert.getDistance() > u_Vert.getDistance() + edges[(u,v)]:
            return None, True

    return G, neg_cycle


def johnson_algorithm(G:myGraph):
    """find all-pairs shortest paths, using Johnson's algorithm, complexity is O(V·E·lgV)"""
    from copy import deepcopy
    G_augment :myGraph = deepcopy(G) # 增广图
    for vertName in G_augment.getVertices(): # 增加辅助节点
        G_augment.addEdge('augVert',vertName,0)
    
    # 使用Bellman-Ford算法，检查是否存在负环
    G_augment, neg_cycle = Bellman_Ford(G_augment, G_augment.getVertex('augVert') ) 
    
    if neg_cycle:
        print('The input graph contains at least a negative-weight cycle!')
        return None
    else:
        from collections import defaultdict
        def return0():
            return 0
        h = defaultdict(return0)
        for vertName in G_augment.getVertices(): # 以B-F算法的单源最短路径长度作为启发式
            vert :Vertex = G_augment.getVertex(vertName)
            h[vertName] = vert.getDistance()
            
        # 对原图中的每一条边进行reweighting
        for vertName in G.getVertices():
            currentVert :Vertex = G.getVertex(vertName)
            for nextVert in currentVert.getConnections():
                newWeight = currentVert.getWeight(nextVert) + h[vertName] - h[nextVert]
                G.setWeight(vertName,nextVert,newWeight)
        
        vertices = G.getVertices()
        n = len(vertices)
        allPairsShortestPath = np.zeros((n,n)) # 用于存储所有点之间的最短路径
        allPairsShortestPath = pd.DataFrame(allPairsShortestPath,index=vertices,columns=vertices)
        allPairsShortestPath = allPairsShortestPath.astype('object')
        
        # 对图中的每一个节点执行Dijkstra算法
        for vertName in G.getVertices():
            # currentVert = G.getVertex(vertName)
            loc_path_dist = oneToAllShortestPath(G, vertName) # 基于Dijkstra实现的单源最短路径算法
            for item in loc_path_dist:
                terminalName, path, dist = item
                realDist = dist + h[terminalName] - h[vertName]
                allPairsShortestPath.loc[vertName,terminalName] = (path,realDist)

        allPairsShortestPath.to_json('allPairsShortestPath.json')

        return allPairsShortestPath
    
def shortedPathBetweenTwoPoints_by_Johnson(G:myGraph, fromName:str, toName:str):
    """给定图，以及开始节点的名称与目标节点的名称，返回最短路径以及最短路径的长度，
    基于Johnson算法实现。第一次调用该函数时计算各节点之间的最短路径，
    并将路径信息保存为json文件。之后调用则直接从本地读取json文件，不再重复计算，节省运算量。
    """
    try: # 如果已经计算过所有点之间的最短路径，则可以直接读取json文件，无需重复计算
        allPairsShortestPath = pd.read_json('allPairsShortestPath.json')
    except Exception:
        allPairsShortestPath = johnson_algorithm(G)
    finally:
        path, distance = allPairsShortestPath.loc[fromName,toName]

    return path, distance


def main():
    g = createGraph()
    while True:
        start = input('请输入起点：')
        terminal = input('请输入终点：')
        path,distance = shortedPathBetweenTwoPoints_by_Johnson(g,start,terminal)
        print('路径为：')
        for v in path:
            print(v,'-->',end='')
        print('\n距离为：',distance)
        print()

if __name__ == '__main__':
    main()