"""
提供了改编自python的Graph类的myGraph类，有更多丰富功能；
提供了基于树结构实现的并查集，查找时进行路径压缩，效率很高；
提供了createGraph函数，能够把助教提供的edges.txt文件转换为myGraph实例；
提供了pointsToCoordinates函数，用于辅助前端的绘图
"""


class Vertex:
    def __init__(self,num):
        self.id = num
        self.connectedTo = {}
        self.color = 'white'
        self.dist = float('inf')
        self.pred = None
        self.disc = 0
        self.fin = 0

    # def __lt__(self,o):
    #     return self.id < o.id
    
    def addNeighbor(self,nbr,weight=0):
        self.connectedTo[nbr] = weight
        
    def setColor(self,color):
        self.color = color
        
    def setDistance(self,d):
        self.dist = d

    def setPred(self,p):
        self.pred = p

    def setDiscovery(self,dtime):
        self.disc = dtime
        
    def setFinish(self,ftime):
        self.fin = ftime
        
    def getFinish(self):
        return self.fin
        
    def getDiscovery(self):
        return self.disc
        
    def getPred(self):
        return self.pred
        
    def getDistance(self):
        return self.dist
        
    def getColor(self):
        return self.color
    
    def getConnections(self):
        return self.connectedTo.keys()
        
    def getWeight(self,nbr):
        return self.connectedTo[nbr]
                
    def __str__(self):
        return str(self.id) + ":color " + self.color + ":disc " + str(self.disc) + ":fin " + str(self.fin) + ":dist " + str(self.dist) + ":pred \n\t[" + str(self.pred)+ "]\n"
    
    def getId(self):
        return self.id


class myGraph:
    def __init__(self):
        self.vertices = {}
        self.numVertices = 0
        
    def addVertex(self,key):
        self.numVertices = self.numVertices + 1
        newVertex = Vertex(key)
        self.vertices[key] = newVertex
        return newVertex
    
    def getVertex(self,n):
        if n in self.vertices:
            return self.vertices[n]
        else:
            return None

    def __contains__(self,n):
        return n in self.vertices
    
    def addEdge(self,f,t,cost=0):
            if f not in self.vertices:
                nv = self.addVertex(f)
            if t not in self.vertices:
                nv = self.addVertex(t)
            self.vertices[f].addNeighbor(self.vertices[t],cost)
    
    def getVertices(self):
        return list(self.vertices.keys())
        
    def __iter__(self):
        return iter(self.vertices.values())
                

    def setWeight(self,fromName:str,toName:str,weight=0):
        f :Vertex = self.getVertex(fromName)
        f.connectedTo[toName] = weight

    def shortestPathTo(self,terminal:Vertex): 
        """用于single-source shortest path问题，
        给定终点，返回从起点到终点路径，以及路径长度，用于Dijkstra算法"""
        v :Vertex = terminal
        path = []
        while v is not None:
            path.append(v.id)
            v = v.pred
        path = list(reversed(path))
        return path, terminal.getDistance()
    
    def showMinimumSpanningTree(self,start:Vertex):
        """用于将最小生成树所包含的边以及最短距离返回，用于Prim算法"""
        edges = []
        distance = 0
        for vertName in self.getVertices(): 
            # 遍历所有节点，注意到在MST中，每个节点要么有一个前驱，有么没有
            currentVert :Vertex = self.getVertex(vertName)
            predVert :Vertex = currentVert.getPred()
            if predVert is None: # 说明是起点
                continue
            edges.append( ( predVert.getId(), currentVert.getId() ) ) # 将这条边加入edges
            distance += predVert.getWeight(currentVert)
        return edges, distance
    
    def getEdges(self) -> dict:
        """返回图中所有的边及其距离，用于Kruskal算法
        返回形式为默认字典，{(u,v): weight}
        若边不存在则weight = float('inf')
        """
        from collections import defaultdict
        def noEdgeExist():
            return float('inf')
        edges = defaultdict(noEdgeExist)

        for vertName in self.getVertices(): # 遍历图中所有节点
            currentVert :Vertex = self.getVertex(vertName)
            neighbours = currentVert.getConnections()
            for nbr in neighbours:
                edges[(vertName,nbr.id)] = currentVert.getWeight(nbr)
        
        return edges


class DisjSet:
    """并查集"""
    def __init__(self, items:list):
        """初始化并查集，每个元素自己成为一个集合，每个元素的前驱都是自己"""
        n = len(items)
        self.rank = dict.fromkeys(items,0) # rank表示树高
        self.parent = {key:value for key, value in zip(items, items)} # 初始时每个元素的前驱都是自己

    def find(self, x):
        """寻找x所在集合的代表元，即树的根节点，并进行路径压缩"""
        if (self.parent[x] != x):
            # call the find method recursively to find the representive of the set
            # and make path compression
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def Union(self, x, y):
        """合并x和y所在的集合"""

        # Find the representative of the sets where x and y respectively belong to 
        xset = self.find(x) # 代表元
        yset = self.find(y) # 代表元

        # If they are already in same set
        if xset == yset:
            return

        # Put smaller ranked item under bigger ranked item if ranks are different
        if self.rank[xset] < self.rank[yset]:
            self.parent[xset] = yset

        elif self.rank[xset] > self.rank[yset]:
            self.parent[yset] = xset

        # If ranks are same, then move y under x (doesn't matter which one goes where)
        # and increment rank of x's tree
        else:
            self.parent[yset] = xset
            self.rank[xset] = self.rank[xset] + 1



def createGraph():
    """读取助教提供的edge.txt文件，并转换成myGraph实例"""
    g = myGraph()
    with open('edge.txt','r') as f:
        for line in f:
            f,t,cost = line.split()
            # print(f,t,cost)
            cost = float(cost)
            g.addEdge(f,t,cost)
            g.addEdge(t,f,cost) # 双向图
    return g


vertexList = []
with open('vertex.txt','r') as f:
    for line in f:
        x , y = eval(line.strip())
        vertexList.append((x,y))

global pointNames
pointNames = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
global pointsLocation
pointsLocation = dict(zip(pointNames,vertexList))

def pointsToCoordinates(u:str,v:str):
    """给定两个标记点的名称u和v，返回u和v的x坐标，以及u和v的y坐标；
    即返回：(u_x,v_x), (u_y,v_y)；
    用于辅助matplotlib绘图"""
    global pointsLocation
    u_coord = pointsLocation[u]
    v_coord = pointsLocation[v]
    xx = (u_coord[0],v_coord[0])
    yy = (u_coord[1],v_coord[1])
    return xx, yy

def findClosestPoints(x,y):
    """given coordinates x and y, find the name of the closest point in the map"""
    global pointsLocation, pointNames
    minDist = float('inf')
    closestPointName = None
    for pointName in pointNames:
        pos_x, pos_y = pointsLocation[pointName]
        Dist = (pos_x -x)**2 + (pos_y - y)**2
        if Dist < minDist:
            minDist = Dist
            closestPointName = pointName
    return closestPointName


def checkValidPoint(vName):
    """check where the name of the vertex is valid"""
    global pointNames
    return len(vName) == 1 and vName in pointNames


def pathsToEdges(loc_path_dist,G_edges):
    """给定一些路径，返回去重后的边，以及总的长度，用于操作四，转化Dijkstra的返回结果"""
    totalDist = 0
    edges = []
    for item in loc_path_dist:
        _, path, dist = item
        for index, u in enumerate(path):
            if index == len(path) - 1:
                break
            v = path[index+1]
            if (u,v) in edges or (v,u) in edges:
                continue
            edges.append((u,v))
            totalDist += G_edges[(u,v)]
    return edges,totalDist



if __name__ == '__main__':
    xx,yy = pointsToCoordinates('A','B')
    print(xx,yy)
