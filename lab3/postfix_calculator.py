from pythonds.basic import Stack

def op_calculate(op1,op2,operator):
    if operator == '+':
        return op1 + op2
    if operator == '-':
        return op1 - op2
    if operator == '*':
        return op1 * op2
    if operator == '/':
        return op1 // op2 # 只进行整数除法


def postfix_calculator(postfix_expression):
    tokens = postfix_expression.split()
    numStack = Stack()
    operators = ['+','-','*','/']
    for token in tokens:
        if token not in operators: # token是数字
            numStack.push(int(token))
        else: # token是运算符
            op2 = numStack.pop()
            op1 = numStack.pop() 
            numStack.push(op_calculate(op1,op2,token))
    return numStack.pop()

def main():
    while True:
        s = input('请输入后序表达式：')
        input(postfix_calculator(s))


if __name__ == '__main__':
    main()