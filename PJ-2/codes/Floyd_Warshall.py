from utils import myGraph, Vertex, createGraph
from collections import defaultdict
import numpy as np
import pandas as pd

def Floyd_Warshall_algorithm(G:myGraph):
    """find all-pairs shortest paths, using Floyd-Warshall algorithm, complexity is O(|V|^3)"""
    vertices = G.getVertices()
    edges :defaultdict = G.getEdges()
    def getWeight(index1, index2):
        u = vertices[index1]
        v = vertices[index2]
        return edges[(u,v)]
    
    n = len(vertices)
    D = np.zeros((n,n))
    D = pd.DataFrame(D,index=vertices,columns=vertices)

    Pi = np.zeros((n,n), dtype=np.int32) * np.nan
    Pi = pd.DataFrame(Pi, index=vertices, columns=vertices)

    for i in range(n): # D_0, Pi_0, initialization
        for j in range(n):
            if i == j:
                D.iloc[i,j] = 0
                continue
            D.iloc[i,j] = getWeight(i,j)
            if D.iloc[i,j] < float('inf'):
                Pi.iloc[i,j] = i

    for k in range(1,n): 
        D_previous = D.copy()
        Pi_previous = Pi.copy()
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                if D_previous.iloc[i,j] <=  D_previous.iloc[i,k] + D_previous.iloc[k,j]:
                    D.iloc[i,j] = D_previous.iloc[i,j]
                else: # D_previous[i,j] >  D_previous[i,k] + D_previous[k,j]
                    D.iloc[i,j] = D_previous.iloc[i,k] + D_previous.iloc[k,j]
                    Pi.iloc[i,j] = Pi_previous.iloc[k,j] # 路径更新，这个地方要看书，ppt上没讲清楚

    D.to_json('shortest_distance.json')
    Pi.to_json('shortest_path.json')

    return D, Pi

def shortedPathBetweenTwoPoints_by_FW(G:myGraph, fromName:str, toName:str):
    """给定图，以及开始节点的名称与目标节点的名称，返回最短路径以及最短路径的长度，
    基于Floyd-Warshall算法实现。第一次调用该函数时计算各节点之间的最短路径，
    并将路径信息保存为json文件。之后调用则直接从本地读取json文件，不再重复计算，节省运算量。
    """

    try: # 如果已经计算过所有点之间的最短路径，则可以直接读取json文件，无需重复计算
        D = pd.read_json('shortest_distance.json')
        Pi= pd.read_json('shortest_path.json')
    except Exception:
        D, Pi = Floyd_Warshall_algorithm(G)
    finally:
        # D, Pi = Floyd_Warshall_algorithm(G)
        vertices = D.columns.tolist()
        fromIndex = vertices.index(fromName)
        toIndex = vertices.index(toName)
        distance = D.iloc[fromIndex,toIndex] # 路径长度
        path = [toName] # 路径
        if fromIndex == toIndex: # 起点和终点相同
            return path, distance
        if D.iloc[fromIndex,toIndex] < float('inf'): # 如果存在路径
            predIndex = int(Pi.iloc[fromIndex,toIndex])
            while predIndex != fromIndex:
                path.insert(0,vertices[predIndex]) # 将该节点名称加入最短路径中 
                predIndex = int(Pi.iloc[fromIndex,predIndex])
            path.insert(0,fromName)
    
    return path, distance


def main():
    g = createGraph()
    while True:
        start = input('请输入起点：')
        terminal = input('请输入终点：')
        path,distance = shortedPathBetweenTwoPoints_by_FW(g,start,terminal)
        print('路径为：')
        for v in path:
            print(v,'-->',end='')
        print('\n距离为：',distance)
        print()

if __name__ == '__main__':
    main()