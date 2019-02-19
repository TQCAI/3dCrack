from scipy.misc import imsave
import cv2
import numpy as np
import pylab as plt
from skimage import morphology
import os
import pandas as pd
from pyautocad import *
from ComputationalGeometry import *

try:
    acad = Autocad(False, True)
    acad.prompt("Hello, Autocad from Python\n")
    print(acad.doc.Name)
except BaseException:
    pass

def testInsertX():
    ps=PointSet((0,1),(3,-1),(8,9))
    # ps.display('scatter')
    # plt.show()
    # st=ps.insertX(1)
    # ps.display('scatter')
    # plt.show()
    st=ps.insertX(7,0)
    ps.display('scatter')
    plt.show()

def displayLine(index):
    df=pd.read_csv("csv/%04d.csv"%index)
    x=df["X"]
    y=df["Y"]
    plt.plot(x, y)
    plt.scatter(x, y,linewidths=0.5)

def peekCsv():
    for i in range(442,500+1):
        name="csv/%04d.csv" % i
        if os.path.exists(name):
            df = pd.read_csv(name)
            print(df["X"].__len__())
    fig = plt.figure(1)
    plt.xlim(640)
    plt.ylim(640)
    displayLine(443)
    displayLine(446)
    # displayLine(447)
    # displayLine(448)
    # displayLine(449)
    # displayLine(450)
    plt.show()

def DeleteAll():
    # try:
    for dgx in acad.iter_objects():
        dgx.Delete()

def Draw3Dpoly(*args):
    # acad.model.Add3Dpoly(aDouble([0, 0, 0, 10, 10, 10, 30, 20, 30, 0, 0, 0]))
    li=[]
    for pt,z in args:
        li+=[pt[0],pt[1],z]
    pt,z=args[0]
    li += [pt[0], pt[1], z]
    acad.model.Add3Dpoly(aDouble(li))

def draw3dCrack1(ps,z,th=5,dz=1):
    '''
    输入两个点集数据，在CAD模型空间中绘制一层三维裂缝
    :param ps: 点集1,2
    :param th:  阈值，超过此阈值就需要拟合
    :param z:   ps1的z坐标
    :return: None
    '''
    l=[0,0]
    l[0]=len(ps[0]);l[1]=len(ps[1])
    Z=[z,z+dz]
    if l[0]>l[1]:   #保证ps0点集数小于ps1点集数
        l.reverse()
        ps.reverse()
        Z.reverse()
    d=l[1]-l[0]
    if d==0:
        for i in range(1,l[0]):
            Draw3Dpoly((ps[0][i-1],Z[0]),
                       (ps[0][i ], Z[0]),
                       (ps[1][i-1 ], Z[1]))
            Draw3Dpoly((ps[0][i ], Z[0]),
                       (ps[1][i ], Z[1]),
                       (ps[1][i-1 ], Z[1]))
    elif d==1:
        for i in range(1,l[0]):
            Draw3Dpoly((ps[0][i-1],Z[0]),
                       (ps[0][i ], Z[0]),
                       (ps[1][i-1 ], Z[1]))
            Draw3Dpoly((ps[0][i ], Z[0]),
                       (ps[1][i ], Z[1]),
                       (ps[1][i-1 ], Z[1]))
        #最后加个三角形
        l=l[0]-1
        Draw3Dpoly((ps[0][l], Z[0]),
                   (ps[1][l+1], Z[1]),
                   (ps[1][l], Z[1]))
    elif d==2:
        pass
    elif d>2 and d<=th:
        pass
    else:   #渐变拟合
        pass

def draw3dCrack(ps,z,th=5,dx=4,dz=1):
    '''
    输入两个点集数据，在CAD模型空间中绘制一层三维裂缝
    :param ps: 点集1,2
    :param th:  阈值，超过此阈值就需要拟合
    :param z:   ps1的z坐标
    :return: None
    '''
    l=[0,0]
    l[0]=len(ps[0]);l[1]=len(ps[1])
    Z=[z,z+dz]
    if l[0]>l[1]:   #保证ps0点集数小于ps1点集数
        l.reverse()
        ps.reverse()
        Z.reverse()
    a=max(ps[0][0].x,ps[1][0].x)
    b=min(ps[0][-1].x,ps[1][-1].x)
    st=[0,0];f=[0,0];X=[0,0]
    for i in range(a,b+dx,dx):
        for j in [0,1]:
            if not ps[j].containX(i):
                # xi=ps[j].getIndexOfX(i)
                st[j]=ps[j].insertX(i,st[j])
                # print('insert')
    X[0], _ = ps[0].getXY();X[1],_=ps[1].getXY()
    f[0] = X[0].index(a);f[1]=X[1].index(a)
    L=(b-a)//dx +1
    for i in range(1,L):
        ix=[0,0]
        ix[0] = f[0] + i;ix[1]=f[1]+i
        Draw3Dpoly((ps[0][ix[0] - 1], Z[0]),
                   (ps[0][ix[0]], Z[0]),
                   (ps[1][ix[1] - 1], Z[1]))
        Draw3Dpoly((ps[0][ix[0]], Z[0]),
                   (ps[1][ix[1]], Z[1]),
                   (ps[1][ix[1] - 1], Z[1]))

def df2ps(df):
    X=list(df.X)
    Y=list(df.Y)
    return PointSet(*list(zip(X,Y)))

def test_a_loop():
    df1=pd.read_csv('csv/0443.csv')
    df2=pd.read_csv('csv/0446.csv')
    # df2=df1.cop y()
    # df2=df2.iloc[1:]
    draw3dCrack([df2ps(df1),df2ps(df2)],0,dz=10)
    # ps0=PointSet((2,3),(10,9),(18,5))
    # ps1=PointSet((6,4),(14,1))
    # draw3dCrack([ps0,ps1],0)


if __name__ == '__main__':
    # DeleteAll()
    df_list=[]
    for i in range(442,500+1):#442 500
        name="csv/%04d.csv" % i
        if os.path.exists(name):
            df = pd.read_csv(name)
            df_list.append(df)
    dz_=10
    z_=0
    for i in range(1,len(df_list)):
        print(i)
        draw3dCrack([df2ps(df_list[i-1]), df2ps(df_list[i])], z=z_, dz=dz_)
        z_+=dz_



