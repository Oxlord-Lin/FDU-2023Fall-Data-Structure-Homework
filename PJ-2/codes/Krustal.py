"""并查集，以及Krustal算法，解决最小生成树问题"""

from utils import myGraph, Vertex, DisjSet, createGraph
# from pythonds.graphs import Vertex


def kruskal(G:myGraph):
    """kurskal算法，也称避圈法，基于并查集找出最小生成树，返回最小生成树包含的边长，以及总的路径长度"""
    MST_edges = [] # 用于存储最小生成树的边
    distance = 0 # 用于存储最小生成树的所有边的路径长度之和
    disjointSet = DisjSet(G.getVertices()) # 并查集，初始化时传入所有节点的名称
    edges = G.getEdges() # 图中所有的边
    # sort the edges into nondecreasing order by their weight
    sortedEdges = sorted(edges.keys(),key=lambda uv : edges[uv]) 
    for e in sortedEdges:
        u,v = e
        if disjointSet.find(u) != disjointSet.find(v): # 如果u和v还未在同一个集合中，则加入这条边
            MST_edges.append(e)
            disjointSet.Union(u,v)
            uVert :Vertex = G.getVertex(u)
            vVert :Vertex = G.getVertex(v)
            distance += uVert.getWeight(vVert)

    return MST_edges, distance 


def main():
    g = createGraph()
    edges, distance = kruskal(g)
    print(edges)
    print('距离为：',distance)

if __name__ == '__main__':
    main()