# 第三版用来接鼠标控制器来实现自动点击.并且结合游戏运行

import shutil

#================
# bug 汇总:
#   1.  看到主要是cv的问题没有做完美, flood迷宫算法没问题
#       cv问题是, 第一个maze 的右下角坐标有时候识别不出来. 考虑调节参数
#                 第二个是切割完小图之后,比较不出来两个相同图片,跟之前担心的一样,差一个像素位置偏差时候很麻烦.
#  2.有兴趣的哥们可以试着优化一下这2点. 先分享版本到这.有时间继续优化.
#
#  3. 洗牌之后的算法需要重新修改. 需要判断黑块.
#
#
#
#
#
#
#
#





#=======
test=0 # 切换用自己图片测试模式还是游戏模式








import cv2
import time
# time.sleep(3) # 启动代码3秒内切到连连看界面
littlepic=57,66  # 点击的方块大小. 单位像素.用画图软件可以自己量.
# 游戏在小游戏/llkwqb里面.
# 首先我们把练练看放到屏幕左上角位置.
print(littlepic)

import numpy as np
from PIL import ImageGrab
import cv2

# BOX = (0, 40, 880, 640)

# 左上角坐标和右下角坐标
# 调整box的值即可改变截取区域

if 0:
    screen = np.array(ImageGrab.grab())[:1200,:1300]  # 1200足够放连连看了.

#=========经过测试imageGrab的像素很低.质量太差了! 改为用下面这个方法来解平.
#==============截取屏幕.
# 下面是截取屏幕的算法.


debug_screen=[]
def getmaze():
    import pyautogui
    import cv2

    img = pyautogui.screenshot()  # x,y,w,h
    # img.save('screenshot.png')
    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

    screen=img[:1200,:1300]
    global debug_screen

    if test: # 使用保存好的图片调试用
        screen=cv2.imread('3.png')[:1200,:1300]
        debug_screen = screen
    cv2.imwrite('tmp.png',screen) # 图像切割.
    # print(screen)
    #===========找到游戏操作的图版的左上和右下. 图版的含义是你一堆littlepic拼起来的区域.
    # littlepic是 那些小图片. 目标就是小图片一样的都点一下.


    # 找到第一个像素点他的 左边50全是黑.
    flag=0
    width,height,channel=screen.shape
    for i in range(width-littlepic[1]):
        if flag==1:
            break
        for j in range(50,height//2):
            tmp=screen[i,j-50:j]
            if np.all(tmp==0)  and tmp.shape[0]==50 and np.all(screen[i:i+7,j:j+7]!=0):
                print(i,j)
                flag=1
                cv2.imwrite('tmp2.png', screen[:i+10,:j+10])  # 图像切割.
                break

    zuoshangjiao=[i,j]
    print(1111111111)

    #==========同理找到右下角.

    # 找到第一个像素点他的 左边50全是黑.
    flag=0
    width,height,channel=screen.shape
    for i in range(width-littlepic[1],0,-1):
        if flag==1:
            break
        for j in range(height-littlepic[0],50,-1):
            tmp=screen[i,j:j+35]
            if np.all(tmp==0)  and tmp.shape[0]==35 and np.all(screen[i-7:i,j-7:j]!=0):
                print(i,j)
                flag=1
                cv2.imwrite('tmp3.png', screen[:i-10,:j-10])  # 图像切割.
                break

    youxiajiao=[i,j]
    print('zuojiao',zuoshangjiao,'youxiajiao',youxiajiao)


    tmp4=screen[zuoshangjiao[0]:youxiajiao[0],zuoshangjiao[1]:youxiajiao[1]]

    cv2.imwrite('tmp4.png',screen[zuoshangjiao[0]:youxiajiao[0],zuoshangjiao[1]:youxiajiao[1]])
    tmp4 = cv2.cvtColor(tmp4, cv2.COLOR_BGR2GRAY)
    #cv2.THRESH_OTSU 可以优化阈值的选择.
    ret,thresh1 = cv2.threshold(tmp4,127,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)



    cv2.imwrite('tmp5.png',thresh1)  # 图像切割.
    tmppic=thresh1
    #======找到所有的水平数值的切割.
    #============找到水平的横线. 都是0的一行

    hang=[]
    for i in range(thresh1.shape[0]):
        if np.all(thresh1[i,:]==0):
          hang.append(i)


    #=========进行像素合并. 找间断的,然后取中值

    hang_after_fix=[]

    savelist=[]

    for i,j in enumerate(hang):
        if i==0:
            savelist.append(j)
            continue
        if j-hang[i-1]==1:
            savelist.append(j)
        else:
            hang_after_fix.append(sum(savelist)/len(savelist))
            savelist=[]
            savelist.append(j)
        #======最后一行别忘了
        if i==len(hang)-1:
            hang_after_fix.append(sum(savelist) / len(savelist))
            savelist = []
    print(hang_after_fix)













    lie=[]
    for i in range(thresh1.shape[1]):
        if np.all(thresh1[:,i]==0):
          lie.append(i)


    #=========进行像素合并. 找间断的,然后取中值

    lie_after_fix=[]

    savelist=[]

    for i,j in enumerate(lie):
        if i==0:
            savelist.append(j)
            continue
        if j-lie[i-1]==1:
            savelist.append(j)
        else:
            lie_after_fix.append(sum(savelist)/len(savelist))
            savelist=[]
            savelist.append(j)
        #======最后一行别忘了
        if i==len(lie)-1:
            lie_after_fix.append(sum(savelist) / len(savelist))
            savelist = []
    print(lie_after_fix)

    #索引int化.
    hang_after_fix=[int(i) for i in hang_after_fix]
    lie_after_fix=[int(i) for i in lie_after_fix]



    #==============下面进行切割小图, 然后存下来,debug用

    dic_all_pic={}
    qipansize=len(hang_after_fix)-1,len(lie_after_fix)-1
    # tmppic 是 棋盘
    for i in range(len(hang_after_fix)-1):
        for j in range(len(lie_after_fix)-1):
            tmp=tmppic[hang_after_fix[i]:hang_after_fix[i+1],lie_after_fix[j]:lie_after_fix[j+1]]
            # cv2.imwrite(f'fordebug/{i}_{j}.png',tmp)
            dic_all_pic[f'{i}_{j}']=tmp


    #=======下面对切割完的进行比较和编码


    print(1)
    #========每个相同的小图之间可能差一些黑色框.所以把矩阵周围一圈黑色都去除.
    for i,j in dic_all_pic.items():
        hang_del,lie_del=[],[]
        for i1 in range(j.shape[0]):
            if np.all(j[i1,:]==0):
                hang_del.append(i1)
        for i1 in range(j.shape[1]):
            if np.all(j[:,i1]==0):
                lie_del.append(i1)
        j=np.delete(j,hang_del,0)
        j=np.delete(j,lie_del,1)
        dic_all_pic[i]=j






    #==========编码
    all_pic=list(dic_all_pic.values())




    # ==========修剪小图片的shape .有时候会差像素.可能因为二值化.都按照最小的切割试试
    xmin = min([i.shape[0] for i in all_pic])
    ymin = min([i.shape[1] for i in all_pic])

    all_pic=[i[:xmin,:ymin] for i in all_pic]





    #========save little pic for debug
    shutil.rmtree('fordebug')
    import os
    os.mkdir('fordebug')
    for i in dic_all_pic:
        cv2.imwrite(f'fordebug/{i}.png',dic_all_pic[i])

    all_pic_del_dup=[] # 记录的是索引
#================================这个地方需要优化比较算法!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    for i in range(len(all_pic)):
        print(f'当前计算的索引是第{i//qipansize[1]}行图片,{i%qipansize[1]}列的图片',)
        dex=[i//qipansize[1],i%qipansize[1]]
        for j in ((all_pic_del_dup)):

            #  有时候切分会差几个像素!
            if np.sum(all_pic[i]!=all_pic[j])<5:#两个图片相同

                all_pic_del_dup.append(j)
                break
        else: # 如果不走break时候才走else. for-else结构非常实用.
          all_pic_del_dup.append(i)

    all_pic_del_dup=np.array(all_pic_del_dup)
    all_pic_del_dup.resize(qipansize)
    print(1)








    print(1)


    #==================下面解这个矩阵.


    # 首先最外一圈补 -1 ,对角线不用补. 不允许走斜线.但是矩阵缺位置更难描述.所以还是都补上

    #=========使用图片的maze
    maze=all_pic_del_dup+1

    # print(1)
    maze2=np.ones([maze.shape[0]+2,maze.shape[1]+2])*0
    maze2[1:-1,1:-1]=maze
    # print(1)
    maze=maze2
    maze=[list(i) for i in maze]
    print("下面打印图片给的maze",maze)          #========以上就是获取maze的代码
    with open('maze.txt','w') as f:
        for i in maze:
            f.write(str(i)+'\n')

    return maze, zuoshangjiao, youxiajiao












def getmaze2(): # 非第一次的getmaze就不要再算zuoshangjiao,youxiajiao, 仍然使用第一次的zuoshangjia youxiajia
    import pyautogui
    import cv2

    img = pyautogui.screenshot()  # x,y,w,h
    # img.save('screenshot.png')
    img = cv2.cvtColor(np.asarray(img), cv2.COLOR_RGB2BGR)

    screen=img[:1200,:1300]
    global debug_screen

    if test: # 使用保存好的图片调试用
        screen=cv2.imread('3.png')[:1200,:1300]
        debug_screen = screen
    cv2.imwrite('tmp.png',screen) # 图像切割.
    # print(screen)
    #===========找到游戏操作的图版的左上和右下. 图版的含义是你一堆littlepic拼起来的区域.
    # littlepic是 那些小图片. 目标就是小图片一样的都点一下.


    # 找到第一个像素点他的 左边50全是黑.
    flag=0
    width,height,channel=screen.shape
    for i in range(width-littlepic[1]):
        if flag==1:
            break
        for j in range(50,height//2):
            tmp=screen[i,j-50:j]
            if np.all(tmp==0)  and tmp.shape[0]==50 and np.all(screen[i:i+7,j:j+7]!=0):
                print(i,j)
                flag=1
                cv2.imwrite('tmp2.png', screen[:i+10,:j+10])  # 图像切割.
                break


    print(1111111111)

    #==========同理找到右下角.

    # 找到第一个像素点他的 左边50全是黑.
    flag=0
    width,height,channel=screen.shape
    for i in range(width-littlepic[1],0,-1):
        if flag==1:
            break
        for j in range(height-littlepic[0],50,-1):
            tmp=screen[i,j:j+35]
            if np.all(tmp==0)  and tmp.shape[0]==35 and np.all(screen[i-7:i,j-7:j]!=0):
                print(i,j)
                flag=1
                cv2.imwrite('tmp3.png', screen[:i-10,:j-10])  # 图像切割.
                break


    print('zuojiao',zuoshangjiao,'youxiajiao',youxiajiao)


    tmp4=screen[zuoshangjiao[0]:youxiajiao[0],zuoshangjiao[1]:youxiajiao[1]]

    cv2.imwrite('tmp4.png',screen[zuoshangjiao[0]:youxiajiao[0],zuoshangjiao[1]:youxiajiao[1]])
    tmp4 = cv2.cvtColor(tmp4, cv2.COLOR_BGR2GRAY)
    #cv2.THRESH_OTSU 可以优化阈值的选择.
    ret,thresh1 = cv2.threshold(tmp4,127,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)



    cv2.imwrite('tmp5.png',thresh1)  # 图像切割.
    tmppic=thresh1
    #======找到所有的水平数值的切割.
    #============找到水平的横线. 都是0的一行

    hang=[]
    for i in range(thresh1.shape[0]):
        if np.all(thresh1[i,:]==0):
          hang.append(i)


    #=========进行像素合并. 找间断的,然后取中值

    hang_after_fix=[]

    savelist=[]

    for i,j in enumerate(hang):
        if i==0:
            savelist.append(j)
            continue
        if j-hang[i-1]==1:
            savelist.append(j)
        else:
            hang_after_fix.append(sum(savelist)/len(savelist))
            savelist=[]
            savelist.append(j)
        #======最后一行别忘了
        if i==len(hang)-1:
            hang_after_fix.append(sum(savelist) / len(savelist))
            savelist = []
    print(hang_after_fix)













    lie=[]
    for i in range(thresh1.shape[1]):
        if np.all(thresh1[:,i]==0):
          lie.append(i)


    #=========进行像素合并. 找间断的,然后取中值

    lie_after_fix=[]

    savelist=[]

    for i,j in enumerate(lie):
        if i==0:
            savelist.append(j)
            continue
        if j-lie[i-1]==1:
            savelist.append(j)
        else:
            lie_after_fix.append(sum(savelist)/len(savelist))
            savelist=[]
            savelist.append(j)
        #======最后一行别忘了
        if i==len(lie)-1:
            lie_after_fix.append(sum(savelist) / len(savelist))
            savelist = []
    print(lie_after_fix)

    #索引int化.
    hang_after_fix=[int(i) for i in hang_after_fix]
    lie_after_fix=[int(i) for i in lie_after_fix]



    #==============下面进行切割小图, 然后存下来,debug用

    dic_all_pic={}
    qipansize=len(hang_after_fix)-1,len(lie_after_fix)-1
    # tmppic 是 棋盘
    for i in range(len(hang_after_fix)-1):
        for j in range(len(lie_after_fix)-1):
            tmp=tmppic[hang_after_fix[i]:hang_after_fix[i+1],lie_after_fix[j]:lie_after_fix[j+1]]
            # cv2.imwrite(f'fordebug/{i}_{j}.png',tmp)
            dic_all_pic[f'{i}_{j}']=tmp


    #=======下面对切割完的进行比较和编码


    print(1)
    #========每个相同的小图之间可能差一些黑色框.所以把矩阵周围一圈黑色都去除.
    for i,j in dic_all_pic.items():
        hang_del,lie_del=[],[]
        for i1 in range(j.shape[0]):
            if np.all(j[i1,:]==0):
                hang_del.append(i1)
        for i1 in range(j.shape[1]):
            if np.all(j[:,i1]==0):
                lie_del.append(i1)
        j=np.delete(j,hang_del,0)
        j=np.delete(j,lie_del,1)
        dic_all_pic[i]=j






    #==========编码
    all_pic=list(dic_all_pic.values())




    # ==========修剪小图片的shape .有时候会差像素.可能因为二值化.都按照最小的切割试试
    xmin = min([i.shape[0] for i in all_pic])
    ymin = min([i.shape[1] for i in all_pic])

    all_pic=[i[:xmin,:ymin] for i in all_pic]





    #========save little pic for debug
    # shutil.rmtree('fordebug')
    # import os
    # os.mkdir('fordebug',)
    # for i in dic_all_pic:
    #     cv2.imwrite(f'fordebug/{i}.png',dic_all_pic[i])

    all_pic_del_dup=[] # 记录的是索引
#================================这个地方需要优化比较算法!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    for i in range(len(all_pic)):
        print(f'当前计算的索引是第{i//qipansize[1]}行图片,{i%qipansize[1]}列的图片',)
        dex=[i//qipansize[1],i%qipansize[1]]
        for j in ((all_pic_del_dup)):

            #  有时候切分会差几个像素!
            if np.sum(all_pic[i]!=all_pic[j])<5:#两个图片相同

                all_pic_del_dup.append(j)
                break
        else: # 如果不走break时候才走else. for-else结构非常实用.
          all_pic_del_dup.append(i)

    all_pic_del_dup=np.array(all_pic_del_dup)
    all_pic_del_dup.resize(qipansize)
    print(1)








    print(1)


    #==================下面解这个矩阵.


    # 首先最外一圈补 -1 ,对角线不用补. 不允许走斜线.但是矩阵缺位置更难描述.所以还是都补上

    #=========使用图片的maze
    maze=all_pic_del_dup+1

    # print(1)
    maze2=np.ones([maze.shape[0]+2,maze.shape[1]+2])*0
    maze2[1:-1,1:-1]=maze
    # print(1)
    maze=maze2
    maze=[list(i) for i in maze]
    print("下面打印图片给的maze",maze)          #========以上就是获取maze的代码
    with open('maze.txt','w') as f:
        for i in maze:
            f.write(str(i)+'\n')

    return maze










#========下面走 迷宫问题. 给定初始点和结束点. 给出所有的走法.





# print(1)


step=[(-1,0),(1,0),(0,-1),(0,1)]  # 上, 下, 左, 右 的顺序访问.

# ===========使用flood 算法. 先填充走一个方向的所有结果,再填充走第二个方向的所有结果.然后看是否有相同的即可.



def compare(a,b):  # a  一个numpy数组, b是numpy矩阵
    for i in a:
        if (i==b).all():
            return True
    return False

import copy
def search(maze, index1,index2):
    # 输入一个maze 和 位置(index1, index2) . 然后返回他flood算法走3个方向之后的所有覆盖点.
# 走3个折线.
    # 并且起点和终点之间只允许经过0 或者什么都不经过
    #

    dex=[index1,index2] # 起始索引
    result=[]  # 换了一个新项目环境, 之前的太坑了,乱跑代码.

    #=========经过0个0就可以到的点
    #走一步,如果到达的位置是0, 那么就可以继续按照这个方向走. 否则就只能停止直接写入result

    #使用bfs来处理=======使用queue,比list curd速度要快.

    a=[]
    a.append(dex)
    tmpway=[] # tmpway  是走一个直线的时候经过的位置.
    #==============走一个直线
    #向上走: 对a里面每一个点都一直向上走.
    result=[]
    result.append(dex)
    for k in range(3):
        for i in (a): # python for 循环数组时候不要在循环里面改变数组, 会无限循环下去. # a是上一轮走完4个方向经过的位置
            for j in step: # 4个方向.
                tmp = i
                while 1: # 一直向一个方向走.
                    tmp=[tmp[0]+j[0],tmp[1]+j[1]]
                    if tmp[0]>=0 and tmp[0]<= len(maze)-1 and tmp[1]>=0 and tmp[1]<=len(maze[0])-1: #判断不会走出maze
                        if maze[tmp[0]][tmp[1]]==0: # 如果遇到0了,就可以继续走,仍如a里面
                            if tmp not in tmpway: # tmp不在a中存在

                                 tmpway.append(tmp)
                            if tmp not in result:
                                 result.append(tmp)
                        else:
                            if tmp not in result:
                                result.append(tmp) # 碰到墙了不用走了.并且不允许继续走这个方向了.
                            break
                    else: # 超界了不用走了
                        break
        # a=copy.deepcopy(tmpway)
        a=tmpway.copy() #把可以继续拓展的位置交给下一轮拓展# 这个地方要用copy, 因为数组是传引用的!!!!!!!! 浅拷贝就足够了. 最高层级拷贝就足够用.
        # print('tmpway',tmpway)
        # print("debug",k,result)
                # print(result,999999)
    return result

#测试maze
# maze=np.array([[1,2,3],[1,1,3]])
# #补0
# maze2=np.ones([maze.shape[0]+2,maze.shape[1]+2])*0
# maze2[1:-1,1:-1]=maze
# # print(1)
# maze=maze2
# maze=[list(i) for i in maze]
# print(maze)

# numpy 好像debug有问题. 还是用list来算吧.
# a=search(maze,1,1)  # a就是3个连线后能到达的位置.


#=========然后我们只抽取里面结果位置符合要求的
def find(maze,a,b):
    # 返回值跟:索引a,b 能匹配上答案一样的图片的索引位置的列表
    candidate=search(maze,a,b)
    result=[]
    for i in candidate:
        if i[0]>0 and i[0]<len(maze)-1 and i[1]>0:
            if i[1] < len(maze[0])-1 and maze[i[0]][i[1]] == maze[a][b] :
                if i[0]==a and i[1]==b:#去除自己本身
                    continue
                else:
                  result.append(i)
    return result

# #=================find算法的输出:
# if 0:
#     print('find算法的输出:')
#     print(find(maze,1,10))


#==============下面进行playdemo.
#算法逻辑是玩这个矩阵. maze看做一维数组,优先消除索引小的块.

def play_one_step():
    for i in range(1,len(maze)-1):
        for j in range(1, len(maze[0]) - 1):
            if maze[i][j]!=0:
                a=find(maze,i,j)
                if a!=[]:
                    #=======进行消除运算.
                    maze[i][j]=0
                    maze[a[0][0]][a[0][1]]=0
                    print(f"消除了索引{i}_{j}和{a[0][0]}_{a[0][1]}")
                    print('打印消除后的maze用来debug',np.array(maze))
                    return True
    return False
#========玩10步:
# if 0:
#     for i in range(10):
#         play_one_step()




#========计算每个砖块的像素位置:

# print('zuoshangjiao',zuoshangjiao,'youxiajiao',youxiajiao)
dic_pix={}  # 把砖块索引和对应的像素坐标放到这个地方.
def computePix(): # 输入的a,b的索引是以1开始计数的.因为maze一周已经补0了.
    hang=len(maze)-2
    lie=len(maze[0])-2
    print('hang',hang,'lie',lie)
    # 算坐标.
    gaodu=(youxiajiao[0]-zuoshangjiao[0])/hang
    kuandu=(youxiajiao[1]-zuoshangjiao[1])/lie
    print('gaodu',gaodu,'kuandu',kuandu)



    for i in range(1,hang+1):
        for j in range(1,lie+1):
            dic_pix[f'{i}_{j}']=[zuoshangjiao[0]+(i-1+0.5)*gaodu,zuoshangjiao[1]+(j-1+0.5)*kuandu]
    #==========注意这个结果key是坐标, value是高和宽!!!!!!!!
# computePix()


#
if 0:#========下面代码画图6,用于debug看是否点击准确.
    print(dic_pix)

    point_size = 1
    point_color = (0, 0, 255) # BGR
    thickness = 4 # 可以为 0 、4、8
    kk=dic_pix.values()


    qq=[]
    for ii in kk:
        qq.append([int(i) for i in ii])



    qq=[i[::-1] for i in qq]
    kk=qq
    kk=[tuple(i) for i in kk]

    print('kk',kk)


    cv2.circle(debug_screen, (10,100), point_size, point_color, thickness)
    for point  in kk[:]:
        cv2.circle(debug_screen, point, point_size, point_color, thickness)

    cv2.imwrite('tmp6.png',debug_screen)











# print(a)


#==============下面书写游戏主逻辑



#================ 首先sleep 5秒. 在这个时间内,需要启动游戏并且选择一个难度开始游戏




time.sleep(3)
import mouse

#===========然后游戏获取maze地图.和点击像素的计算. 这些统一叫做预处理.

maze, zuoshangjiao, youxiajiao=getmaze()
computePix()


def play_one_step_trully(): # 在真是环境下玩一步
    for i in range(1,len(maze)-1):
        for j in range(1, len(maze[0]) - 1):
            if maze[i][j]!=0:
                a=find(maze,i,j)
                if a!=[]:
                    #=======进行消除运算.
                    maze[i][j]=0
                    maze[a[0][0]][a[0][1]]=0

                    #========这里进行鼠标点击.
                    mouse.move(dic_pix[f'{i}_{j}'][1],dic_pix[f'{i}_{j}'][0])
                    mouse.click()
                    mouse.move(dic_pix[f'{a[0][0]}_{a[0][1]}'][1],dic_pix[f'{a[0][0]}_{a[0][1]}'][0])
                    mouse.click()


                    print(f"消除了索引{i}_{j}和{a[0][0]}_{a[0][1]}")
                    print('打印消除后的maze用来debug',maze)
                    return True
    return False
play=not test
while play:
    a=play_one_step_trully()
    if a:
        time.sleep(2)
    else:#无解了
        time.sleep(2)
        #重新cv一遍即可.
        maze = getmaze2()
        computePix()

































