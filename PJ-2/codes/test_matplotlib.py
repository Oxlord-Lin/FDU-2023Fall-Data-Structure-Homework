import matplotlib
matplotlib.use('TkAgg') # 可交互
import matplotlib.pyplot as plt
matplotlib.rc("font",family='YouYuan') # 显示中文字体
import cv2 as cv

# fig = plt.figure(figsize=(16,12))
ori_img = cv.imread("tagged.png")

# 选取控制点
plt.subplot(111)
plt.imshow(ori_img)
# plt.title("请您用鼠标点击选择控制点，共26个")
# points = plt.ginput(n=26,timeout=0) # 回车结束选点

# with open('vertex.txt','w') as f:
#     for line in points:
#         f.write(str(line))
#         f.write('\n')


plt.plot((125.58118733704544,241.9790390103879),(378.81250257026045,887.7520747143925),'gold')
plt.plot((931.5359671993617,1043.9200998494857),(948.7606038673168,332.25336190092344),'gold')

plt.imshow(ori_img)
points = plt.ginput(n=26,timeout=0) # 回车结束选点