myDict = {
1:'Internship',
2:'ALL COURSES',
3:'Thesis',
4:'Java or C+',
5:'Web Application',
6:'Object Oriented Programming',
7:'Database',
8:'Software Engineering',
9:'Data Structure and Algorithm',
10:'Computer Architecture',
11:'Computer Systems',
12:'Calculus',
13:'Project Management',
14:'Computer Network',
15:'Intelligent Systems',
16:'Probability and Statistics',
17:'Discrete Mathematics',
}

relations=[
    (2,1),
    (2,3),
    (1,3),
    (4,5),
    (4,6),
    (4,9),
    (9,8),
    (6,8),
    (7,5),
    (7,8),
    (9,15),
    (8,13),
    (8,15),
    (11,8),
    (14,8),
    (11,14),
    (11,10),
    (12,10),
    (12,16),
    (16,15),
    (17,15),
    (16,9),
    (6,5),
]

print('[')
for i in range(1,18):
    print("\'",myDict[i],"\',",sep='')
print(']')


print('[')
for relation in relations:
    pred = relation[0]
    succ = relation[1]
    print(  "(", "\'",  myDict[pred],  "\'" , ", ", "\'", myDict[succ],   "\'",  "),",    sep='')
print(']')