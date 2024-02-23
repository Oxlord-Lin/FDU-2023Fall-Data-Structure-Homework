class vertex():
    """图的节点"""
    def __init__(self,jobName:str,color='white',parent=None,startTime=None,finishTime=None):
        self.job = jobName
        self.color = color # 初始时都为白色，未发现，用于深度搜索和拓扑排序
        self.parent = parent
        self.startTime = startTime
        self.finishTime = finishTime
        self.adj = [] # 邻接节点
        self.accumulatedCost = float('inf') # 从起点到达该点的累计代价


class Graph():
    """建立图，能够执行深度优先搜索和拓扑排序，找到最长路径"""
    def __init__(self,jobNames:str,relations:list,start:str=None,ending:str=None):    # 初始化一张图
        """
        para:jobNames是所有工作的名称
        para:relations是所有工作的先后关系，每个关系都是一个三元组，格式为：（前驱工作，后续工作，消耗时间）
        """
        self.timeCounter = 0  # 计时器，用于计算被发现扩展和结束扩展的时间
        self.jobsNames = jobNames # 所有工作的名称


        self.vertex = dict() # 用于存储图的节点
        self.edgeWeight = dict() # 用于存储图的带权边
        for jobName in jobNames:
            self.vertex[jobName] = vertex(jobName) # 该字典把工作名映射到图节点

        self.start :vertex = self.vertex[start] # 图的起始节点，如果有的话
        self.ending :vertex = self.vertex[ending] # 图的结束节点，如果有的话
        
        for pred, succ, cost in relations:
            pred_vertex = self.vertex[pred] # 找到前驱工作对应的节点
            succ_vertex = self.vertex[succ] # 找到后继工作对应的节点
            pred_vertex.adj.append(succ_vertex) # 把后继工作添加到前驱工作的adj属性中
            self.edgeWeight[(pred,succ)] = cost # 把edge作为键值，把工作时间作为value值，添加到字典中

        self.sortedVertex :list = []  # 用于存储经过拓扑排序后的vertex

    def getStart(self):
        return self.start
    
    def getEnding(self):
        return self.ending

    def DFS(self):
        """执行深度优先搜索，并且会记录每个节点开始探索和结束探索的时间"""
        self.timeCounter = 0
        for jobName in  self.jobsNames: # 每个节点都要作为起点进行一次深度优先搜索，防止出现非连通图的情况
            job_vertex :vertex = self.vertex[jobName] # 把工作名映射到节点
            if job_vertex.color == 'white':
                self._DFSvisit(job_vertex)

    def _DFSvisit(self,current_vertex:vertex):
        """私有函数，辅助深度优先搜索"""
        current_vertex.color = 'gray'
        self.timeCounter += 1
        current_vertex.startTime = self.timeCounter
        for adjVertex in current_vertex.adj:
            if adjVertex.color == 'white': # 邻接节点还没有被探索过
                adjVertex.parent = current_vertex
                self._DFSvisit(adjVertex) # 递归调用深度优先
        current_vertex.color = 'black' # 该节点结束探索
        self.timeCounter += 1
        current_vertex.finishTime = self.timeCounter

    def topologicalSort(self):
        """拓扑排序，按照深度优先搜索的结束时间逆序排列"""
        self.DFS() # 调用DFS，计算各个节点的结束时间
        sortedVertex = []
        for jobName in self.jobsNames: # 把所有节点放入一个列表中
            sortedVertex.append(self.vertex[jobName])
        sortedVertex = sorted(sortedVertex, key=lambda v: v.finishTime, reverse=True)
        self.sortedVertex = sortedVertex # 以列表存储按照拓扑排序后的节点

    def findShortestPath(self):
        """找到从起点出发到各个点的最短路径，基于拓扑序进行更新"""
        self.topologicalSort() # 先进行拓扑排序
        for v in self.sortedVertex: 
            v.accumulatedCost = float('inf') # 初始化
            v.parent = None
        s :vertex= self.getStart() # 起点
        s.accumulatedCost = 0
        for u in self.sortedVertex:
            for v in u.adj:
                if v.accumulatedCost > u.accumulatedCost + self.edgeWeight[(u.job,v.job)]:
                    v.accumulatedCost = u.accumulatedCost + self.edgeWeight[(u.job,v.job)]
                    v.parent = u

    def findLongestPath(self):
        """找到从起点出发到达终点的最长路径，返回最长路径以及用时"""
        for key in self.edgeWeight.keys():
            self.edgeWeight[key] *= -1 # 把所有边的权重都设为相反数
        self.findShortestPath() # 由于各个边的权重取了相反数，则此时找到最短路径就等价于找到最长路径
        for key in self.edgeWeight.keys():
            self.edgeWeight[key] *= -1 # 把边的权重进行还原
        
        # 生成最长路径
        v :vertex = self.getEnding() 
        longestPath = []
        while v is not None:
            longestPath.insert(0,v.job) # 将最长路径上的工作依次添加到列表中
            v = v.parent
        return longestPath, self.ending.accumulatedCost*(-1)
        
        
def criticalPath(jobs,relations,start,ending):
    """
    para:jobs是节点，表示所有的工作
    para:relations表示边，规定了工作的先后关系，以及权重
    para:start是第一个要开始的工作
    para:ending是最后一个工作
    output: 打印出最长的路径，以及相应的用时
    """
    # 构建图
    G = Graph(jobs,relations,start,ending) # Graph是我自己定义的一个类
    # 找到最长路径，并且返回用时
    path, cost = G.findLongestPath()
    print('\n最长路径如下：')
    for job in path[:-1]:
        print(job,'--> ',end='')
    print(path[-1])
    print('路径长度为：',cost)
    


def main():
    # example 1
    jobs1 = ['1','2','3','4','5','6','7','8','9','10']
    relation1 = [('1','2',4),
                 ('1','3',5),
                 ('1','4',4),
                 ('2','7',6),
                 ('2','5',4),
                 ('3','5',5),
                 ('3','6',6),
                 ('4','6',7),
                 ('5','7',3),
                 ('5','8',4),
                 ('6','8',2),
                 ('6','9',2),
                 ('7','10',3),
                 ('8','10',2),
                 ('9','10',5)]
    start1 = '1'
    ending1 = '10'
    criticalPath(jobs1,relation1,start1,ending1)
    # 最长路径如下：
    # 1 --> 4 --> 6 --> 9 --> 10
    # 路径长度为： 18
    
    # example 2
    jobs2 = ['V1','V2','V3','V4','V5','V6']
    relation2=[('V1','V2',3),
               ('V1','V3',2),
               ('V2','V4',2),
               ('V3','V4',4),
               ('V2','V5',3),
               ('V5','V6',1),
               ('V4','V6',2),
               ('V3','V6',3)]
    start2 = 'V1'
    ending2 = 'V6'
    criticalPath(jobs2,relation2,start2,ending2)
    # 最长路径如下：
    # V1 --> V3 --> V4 --> V6
    # 路径长度为： 8


    # example 3
    jobs3 = ['1','2','3','4','5','6']
    relation3 = [('1','2',3),
                 ('1','3',8),
                 ('3','2',4),
                 ('2','4',9),
                 ('3','5',10),
                 ('2','5',6),
                 ('4','6',6),
                 ('5','6',9)]
    start3 = '1'
    ending3 = '6'
    criticalPath(jobs3,relation3,start3,ending3)
    # 最长路径如下：
    # 1 --> 3 --> 5 --> 6
    # 路径长度为： 27


    # example 4
    jobs4 = ['V1','V2','V3','V4','V5','V6','V7','V8','V9']
    relation4 = [('V1','V2',2),
                 ('V1','V3',5),
                 ('V1','V5',5),
                 ('V2','V4',3),
                 ('V3','V6',3),
                 ('V5','V7',6),
                 ('V2','V3',2),
                 ('V3','V5',1),
                 ('V4','V6',2),
                 ('V6','V7',3),
                 ('V6','V8',4),
                 ('V8','V9',2),
                 ('V7','V9',4)]
    start4 = 'V1'
    ending4 = 'V9'
    criticalPath(jobs4,relation4,start4,ending4)
    # 最长路径如下：
    # V1 --> V3 --> V5 --> V7 --> V9
    # 路径长度为： 16


if __name__ == '__main__':
    main()