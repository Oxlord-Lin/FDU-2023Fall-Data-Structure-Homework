import numpy as np

def get_time(job):
    """返回job的消耗时间"""
    return job[0]

def get_profit(job):
    """返回job的收益"""
    return job[1]

def get_ddl(job):
    """返回允许结束的最晚时间"""
    return job[2]


def find_best_schedule(jobs:list):
    """输入可以选择的工作jobs，返回最大的收益，以及最优的工作安排方案"""
    # 输入样例的格式为:
    # jobs = [(t1,p1,d1),(t2,p2,d2),(t3,p3,d3)....]
    jobs_by_ddl = sorted(jobs,key = lambda job:job[2])  # 按照ddl升序排列
    n = len(jobs_by_ddl)
    jobs_by_ddl.insert(0,None) # 使得job的下标从1开始
    # G 是辅助矩阵，用于存储收益
    G = np.zeros((n+1, n**2+1))  # 初始值全部设为零。G的上方和左边的值始终为0
    # Action 用于存储转移关系
    Action = G.copy()
    Action = list(Action)
    for i in range(len(Action)):
        Action[i] = list(Action[i])
    for i in range(1,n+1):
        t_i = get_time(jobs_by_ddl[i])
        p_i = get_profit(jobs_by_ddl[i])
        d_i = get_ddl(jobs_by_ddl[i])
        for j in range(1,n**2+1):
            if j <= d_i and j - t_i >= 0: # 有时间做最后一项工作
                p1 = G[i-1,j] # 最后一项工作不做
                p2 = G[i-1,j-t_i] + p_i # 最后一项工作要做
                if p1 >= p2: # 最后一项工作不做
                    G[i,j] = p1
                    Action[i][j] = (i-1,j,None)
                elif p1 < p2: #要做最后一项工作
                     G[i,j] = p2
                     Action[i][j] = (i-1,j-t_i,i)
            elif j <= d_i and j - t_i < 0: #没有时间做最后一项工作
                G[i,j] = G[i-1,j]
                Action[i][j] = (i-1,j,None)
            elif j > d_i: # 时间太多了，超过最后一项工作的ddl
                G[i,j] = G[i,d_i]
                Action[i][j] = (i,d_i,None)
    
    best_jobs = []
    act = Action[-1][-1] # act是一个三元组
    while True:
        if act[-1] is not None: # 此时选择了某个job
            best_jobs.insert(0,jobs_by_ddl[act[-1]])
            if act[0] == 0 or act[1] == 0:
                break
            act = Action[act[0]][act[1]] # 转移关系
        else: # act[-1] is None:
            if act[0] == 0 or act[1] == 0: # 走到了Action表的边界，退出循环
                break
            act = Action[act[0]][act[1]] # Action表的转移关系

    return G[-1,-1], best_jobs  # 返回最优收益和最佳安排方案
            

def main():
    
    sample_jobs = [
    [(2, 60, 3), (1, 100, 2), (3, 20, 4), (2, 40, 4)],
    [(3, 100, 4), (1, 80, 1), (2, 70, 2), (1, 10, 3)],
    [(4, 100, 4), (2, 75, 3), (3, 50, 3), (1, 25, 1)],
    [(2, 60, 3), (1, 100, 2), (3, 20, 3), (2, 40, 2), (2, 50, 3)],
    [(2, 60, 3), (1, 100, 2), (3, 20, 4), (2, 40, 4), (2, 50, 3), (1, 80, 2)],
    [(2, 60, 3), (1, 100, 2), (3, 20, 3), (2, 40, 2), (2, 50, 3), (1, 80, 2), (4, 90, 4)],
    [(3, 60, 3), (2, 100, 2), (1, 20, 2), (2, 40, 4), (4, 50, 4)],
    [(2, 60, 3), (1, 100, 2), (3, 20, 3), (2, 40, 2), (4, 50, 4), (1, 80, 2), (4, 90, 4)],
    [(3, 60, 3), (2, 100, 2), (1, 20, 2), (2, 40, 2), (4, 50, 4), (5, 70, 5)],
    [(2, 60, 3), (1, 100, 2), (3, 20, 3), (2, 40, 2), (4, 50, 4), (5, 70, 5), (3, 90, 4)]
]

    for jobs in sample_jobs:
        max_profit, schedule = find_best_schedule(jobs)
        s = "\n \item 对于工作${}$，最大的收益为{}，获得最大收益的工作安排方式为${}$".format(jobs,max_profit,schedule)
        print(s)
    
if __name__ == '__main__':
    main()
