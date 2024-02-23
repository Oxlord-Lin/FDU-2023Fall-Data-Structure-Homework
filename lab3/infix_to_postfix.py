from pythonds.basic import Stack  # 需要在终端输入 python -m pip install pythonds 进行安装

def parenthesis_checker(parenthesis):
    s = Stack()
    for par in parenthesis:
        if par == '(':
            s.push(par)
        else: # par == ')'
            if s.isEmpty():
                return False
            temp = s.pop()
            if temp == ')':
                return False
    return s.isEmpty() # 最终栈内应该无括号剩余

def infix_to_postfix(infix_expression):
    """本函数能够检查括号是否匹配，并提供 +加法、-减法、*乘法、/除法、mod 取余数、^求幂运算
    输入：一个中序表达式，要求所有的运算符和运算数之间都用空格间隔，
        例如A + B mod 5 * 8，并要求幂指数部分必须使用括号以示分界，例如A ^ ( 4 + b )     
    输出：一个postfix表达式，其运算优先级为 level(+, -) < level(*, /, mod) < level(^)"""
    tokens = infix_expression.split()
    parenthesis = []
    for token in tokens:
        if token == '(' or token == ')':
            parenthesis.append(token)
    if not parenthesis_checker(parenthesis):  # 如果括号不匹配
        print('表达式的括号匹配有误！')
        return False
    level = {'(':0, ')':0, '+':1,'-':1,'*':2,'/':2,'mod':2,'^':3} # 使用字典存储各个运算符的优先顺序，其中左括号的优先级为0，以保证括号内的运算符能全都入栈
    ops = set(level.keys()) # 所有的运算符
    op_stack = Stack()
    postfix_expression = []
    for token in tokens:
        if token not in ops: # 如果是数字
            postfix_expression.append(token)
        elif token == '(': # 左括号不进行优先级比较，直接入栈
            op_stack.push(token)
        elif token == ')':
            temp = op_stack.pop()
            while temp != '(': # 遇到右括号则不断弹出栈内运算符直到遇见左括号
                postfix_expression.append(temp)
                temp = op_stack.pop()
        else: # 除了左右括号之外的其他运算符
            while (not op_stack.isEmpty()) and (level[op_stack.peek()] >= level[token]): # 当栈还未空时，要不断检查栈顶的运算符优先级
                postfix_expression.append(op_stack.pop()) # 如果栈顶运算符大于等于token，则要把栈顶运算符弹出
            op_stack.push(token)
    while not op_stack.isEmpty(): # 表达式全部读完，把栈内剩余的运算符全部弹出
        postfix_expression.append(op_stack.pop())
    return ' '.join(postfix_expression)     # 返回的逆波兰式用空格连接


def main():
    while True:
        in_s = input('请输入中序表达式：')
        pos_s = infix_to_postfix(in_s)
        print(pos_s)

if __name__ == '__main__':
    main()