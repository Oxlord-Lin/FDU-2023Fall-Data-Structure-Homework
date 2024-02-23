class state():
    """用于表示狼、羊、菜、人的位置状态，
    并且提供判断终点、判断安全、找出相邻状态的功能"""
    def __init__(self,position:list):
        self.position = position # 四元组，分别表示狼、羊、菜、人的位置，0表示在左岸，1表示在右岸

    def isSafe(self) -> bool:
        """判断当前的状态，羊和菜是否都安全，"""
        position = self.position
        # 当人不在的情况下，狼吃羊，羊吃菜
        if position[0] == position[1] and position[0] != position[3]:
            return False
        if position[1] == position[2] and position[1] != position[3]:
            return False
        return True

    def isTerminal(self) -> bool:
        """判断是否已经到达终点"""
        return self.position == [1,1,1,1]

    def findSucc(self) -> list:
        """返回所有安全的下一时刻的状态，若已经到终点，或当前时刻不安全，则返回空列表"""
        if self.isTerminal():
            return []
        if not self.isSafe():
            return []
        # 返回所有安全的下一步position，每个postion是一个四元组列表
        successor = []
        position = self.position
        newPosition = list(position)
        newPosition[3] = (newPosition[3]+1) % 2 # 只有人过河
        newState = state(newPosition)
        if newState.isSafe():
            successor.append(newPosition)
        for i in range(3): # 分别考察农夫把同侧的（狼、羊、菜）运过河的情况
            if position[i] == position[3]: # 如果在同侧
                newPosition = list(position)  
                newPosition[i] = (newPosition[i]+1) % 2
                newPosition[3] = (newPosition[3]+1) % 2
                newState = state(newPosition)
                if newState.isSafe(): # 只考虑安全的状态
                    successor.append(newPosition)
        return successor


class node():
    """压入栈中的节点，既保存图的节点，也保存从起点到当前节点的路径，
    并提供打印路径、判断是否成环的功能"""
    def __init__(self,currentState:state,ancestors=[]):
        self.currentState:state = currentState
        self.ancestors :list = ancestors # 记录从开始状态到目前状态的路径，每个状态都是一个state类
    
    def printPath(self) -> list:
        """返回从开始状态到当前节点的路径"""
        path = list((x.position for x in self.ancestors))
        path.append(self.currentState.position)
        return path
    
    def isSafe(self) -> bool:
        """判断当前节点是否为安全的节点"""
        return self.currentState.isSafe()

    def isTerminal(self) -> bool:
        """判断是否已经到达终点"""
        return self.currentState.isTerminal()
    
    def isCyclic(self) -> bool:
        """判断当前路径是否出现环"""
        for anc in self.ancestors:
            if anc.position == self.currentState.position:
                return True
        return False


def main():
    stack = [] # python的list可以很方便地模拟stack
    start = node(state([0,0,0,0]),[]) # 开始状态
    stack.append(start) 
    while len(stack) > 0: # 不断迭代，直到stack为空
        currentNode:node = stack.pop()
        if currentNode.isTerminal(): # 如果当前节点是终点，则打印从开始状态到终点状态的路径
            print(currentNode.printPath())
            continue

        for suc in currentNode.currentState.findSucc(): # 准备将当前状态的所有安全的子状态加入stack中
            newNode:node = node(currentState=state(suc),ancestors=currentNode.ancestors+[currentNode.currentState])
            if newNode.isCyclic(): # 如果出现环，则不加入
                continue
            else:
                stack.append(newNode)


if __name__ == '__main__':
    main()