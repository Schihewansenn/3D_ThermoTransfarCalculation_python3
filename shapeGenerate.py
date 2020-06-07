import numpy as np
import time
import copy

class Glob :  # 球体类

    def __init__(self):    # 实例化后自身变量
        # 注：本体与模拟空间的边界至少存在1个模拟微元的间隔
        self.sizex = 64  # 模拟空间x方向尺寸
        self.sizey = 64  # 模拟空间y方向尺寸
        self.sizez = 64  # 模拟空间z方向尺寸
        self.R = 30       # 本体球体半径
        self.Tsur = 373  # 环境温度
        self.Tbar = 273  # 本体温度
        # 生成一个模拟空间形状的全零多维数组
        self.StructureArr = np.zeros(self.sizez*self.sizey*self.sizex).reshape(self.sizez, self.sizey, self.sizex)
    
    # 形体矩阵内部绘制
    def insideStructure(self):
        # 勾股定理，循环计算
        l = round(self.sizex / 2)
        m = round(self.sizey / 2)
        n = round(self.sizez / 2)
        for k in range(self.sizez):
            for j in range(self.sizey):
                for i in range(self.sizex):
                    self.r = (i - l)**2 + (j - m)**2 + (k - n)**2
                    if self.r <= self.R**2 :
                        self.StructureArr[k][j][i] = 2

    # 形体边界
    def boundaryStructure(self):
        # 与本体相邻的即为边界
        for k in range(1, self.sizez-1):
            for j in range(1, self.sizey-1):
                for i in range(1, self.sizex-1):
                    if self.StructureArr[k][j][i+1] == 2 and self.StructureArr[k][j][i-1] == 0 :
                        self.StructureArr[k][j][i] = 1
                    elif self.StructureArr[k][j][i-1] == 2 and self.StructureArr[k][j][i+1] == 0 :
                        self.StructureArr[k][j][i] = 1
                    elif self.StructureArr[k][j+1][i] == 2 and self.StructureArr[k][j-1][i] == 0 :
                        self.StructureArr[k][j][i] = 1
                    elif self.StructureArr[k][j-1][i] == 2 and self.StructureArr[k][j+1][i] == 0 :
                        self.StructureArr[k][j][i] = 1
                    elif self.StructureArr[k+1][j][i] == 2 and self.StructureArr[k-1][j][i] == 0 :
                        self.StructureArr[k][j][i] = 1
                    elif self.StructureArr[k-1][j][i] == 2 and self.StructureArr[k+1][j][i] == 0 :
                        self.StructureArr[k][j][i] = 1
                    else :
                        self.StructureArr[k][j][i] = self.StructureArr[k][j][i]

    # 将形体矩阵的值转化为对应温度分布
    def Temp(self):
        self.TempArr = copy.deepcopy(self.StructureArr)
        self.TempArr[self.TempArr == 2] = self.Tbar
        self.TempArr[self.TempArr == 1] = self.Tsur

    # 返回温度分布结果
    def resultTemp(self):
        return self.TempArr

    # 返回形体矩阵结果
    def resultStructure(self):
        return self.StructureArr


t1 = time.time()
s = Glob()
s.insideStructure()
s.boundaryStructure()
s.Temp()
M1 = s.resultTemp()
M2 = s.resultStructure()

np.set_printoptions(threshold=np.inf)
np.save('Tdistribution.npy', M1)
np.save('Structure.npy', M2)
t2 = time.time()

print('结构文件产生完毕')
