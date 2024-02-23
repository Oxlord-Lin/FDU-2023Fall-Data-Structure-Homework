class vertex():
    """图的节点"""
    def __init__(self,courseName:str,color='white',parent=None,startTime=None,finishTime=None):
        self.course = courseName
        self.color = color # 初始时都为白色，未发现
        self.parent = parent
        self.startTime = startTime
        self.finishTime = finishTime
        self.adj = []


class Graph():
    """建立图，并且能够执行深度优先搜索和拓扑排序"""
    def __init__(self,courseNames,relations):    # 初始化一张图
        """
        para:courseNames是所有课程的名称
        para:relations是所有课程的修读关系，每个关系都是一个二元组
        """
        self.timeCounter = 0  # 计时器，用于计算被发现扩展和结束扩展的时间
        self.coursesNames = courseNames
        self.vertex = dict()
        for courseName in courseNames:
            self.vertex[courseName] = vertex(courseName) # 该字典把课程名映射到图节点
        for relation in relations:
            pred, succ = relation
            pred_vertex = self.vertex[pred] # 找到前驱课程对应的节点
            succ_vertex = self.vertex[succ] # 找到后继课程对应的节点
            pred_vertex.adj.append(succ_vertex)

    def DFS(self):
        """执行深度优先搜索，并且会记录每个节点开始探索和结束探索的时间"""
        self.timeCounter = 0
        for courseName in  self.coursesNames:
            course_node :vertex = self.vertex[courseName] # 把课程名映射到节点
            if course_node.color == 'white':
                self._DFSvisit(course_node)

    def _DFSvisit(self,current_vertex:vertex):
        """私有函数，辅助深度优先搜索"""
        current_vertex.color = 'gray'
        self.timeCounter += 1
        current_vertex.startTime = self.timeCounter
        for adjVertex in current_vertex.adj:
            if adjVertex.color == 'white':
                adjVertex.parent = current_vertex
                self._DFSvisit(adjVertex)
        current_vertex.color = 'black'
        self.timeCounter += 1
        current_vertex.finishTime = self.timeCounter

    def topologicalSort(self):
        """拓扑排序，按照深度优先搜索的结束时间逆序排列"""
        self.DFS() # 调用DFS，计算各个节点的结束时间
        Vertex = []
        for c in self.coursesNames: # 把所有节点放入一个列表中
            Vertex.append(self.vertex[c])
        vertexCourses = sorted(Vertex, key=lambda v: v.finishTime, reverse=True)
        return [v.course for v in vertexCourses]


def main():
    # 所有课程
    courses = [
        'Internship',
        'ALL COURSES',
        'Thesis',
        'Java or C+',
        'Web Application',
        'Object Oriented Programming',
        'Database',
        'Software Engineering',       
        'Data Structure and Algorithm',
        'Computer Architecture',
        'Computer Systems',
        'Calculus',
        'Project Management',
        'Computer Network',
        'Intelligent Systems',
        'Probability and Statistics',
        'Discrete Mathematics',
    ]

    # 输入所有课程关系
    # 每个元组表示一个关系，第一个课程是先修课程，后一个课程是后续课程
    relations = [
    ('ALL COURSES', 'Internship'),
    ('ALL COURSES', 'Thesis'),
    ('Internship', 'Thesis'),
    ('Java or C+', 'Web Application'),
    ('Java or C+', 'Object Oriented Programming'),
    ('Java or C+', 'Data Structure and Algorithm'),
    ('Data Structure and Algorithm', 'Software Engineering'),
    ('Object Oriented Programming', 'Software Engineering'),
    ('Database', 'Web Application'),
    ('Database', 'Software Engineering'),
    ('Data Structure and Algorithm', 'Intelligent Systems'),
    ('Software Engineering', 'Project Management'),
    ('Software Engineering', 'Intelligent Systems'),
    ('Computer Systems', 'Software Engineering'),
    ('Computer Network', 'Software Engineering'),
    ('Computer Systems', 'Computer Network'),
    ('Computer Systems', 'Computer Architecture'),
    ('Calculus', 'Computer Architecture'),
    ('Calculus', 'Probability and Statistics'),
    ('Probability and Statistics', 'Intelligent Systems'),
    ('Discrete Mathematics', 'Intelligent Systems'),
    ('Probability and Statistics', 'Data Structure and Algorithm'),
    ('Object Oriented Programming', 'Web Application'),
    ]
    # 建立图，并进行拓扑排序
    G = Graph(courses,relations) # Graph是我自己定义的一个类
    sortedCourse = G.topologicalSort()
    print(sortedCourse)


if __name__ == '__main__':
    main()