import numpy as np
import copy

# 显示数组全部精度
np.set_printoptions(threshold=np.inf)

# 时间偏导数函数
def dirTot(Tdistribution, Guide, Zeromat1, Zeromat2, Zeromat3, MicroDel, alpha):
    # x axis second differance
    B1 = np.diff(Tdistribution, n = 2, axis = -1)
    # y axis second differance 
    B2 = np.diff(Tdistribution, n = 2, axis =  1)
    # z axis second differance
    B3 = np.diff(Tdistribution, n = 2, axis =  0)
    # 构建全零矩阵
    B4 = np.array(Zeromat1)
    B5 = np.array(Zeromat2)
    B6 = np.array(Zeromat3)
    # 切片赋值
    B4[1:-1, :, :] = B3
    B5[: ,1:-1, :] = B2
    B6[:, :, 1:-1] = B1
    # 求解三维二阶差分
    B7 = np.array(B4) + np.array(B5) + np.array(B6)
    # 求解时间-温度偏导数
    B8 =np.array(Guide) * np.array(B7) * alpha / MicroDel**2
    return B8

# 生成与温度分布相同的全零矩阵
def zeromat(Tdistribution):
    Tdistribution = np.array(Tdistribution)
    lenx = Tdistribution.shape[2]
    leny = Tdistribution.shape[1]
    lenz = Tdistribution.shape[0]
    Zeromat = np.zeros(lenx*leny*lenz).reshape(lenz, leny, lenx)
    return Zeromat

# 读取设置脚本，确定计算细节
def setup(filename = 'setup.txt'):
    f1 = open(filename)
    w1 = f1.read()
    f1.close()
    w1 = w1.split(';')
    w2 = []
    for i in w1 :
        j = eval(i)
        w2 = w2 + [j]
    return w2

# 引导数组
def guide(Structure):
    Mat3 = np.array(copy.deepcopy(Structure))
    Mat3[Mat3 == 1] = 0
    Mat3[Mat3 == 2] = 1
    Mat3[Mat3 == 3] = 1
    return Mat3

# 温度变化量矩阵
def dT(DirT, Microtime):
    dt = np.array(DirT) * Microtime
    return dt

# 主程序
print('3D有限元传热计算器开始计算')

# 读取脚本信息，产生初始化列表
Setup = setup()
# 设定微元空间尺寸
MicroDel = Setup[0]
# 设定时间差分量
Microtime = Setup[1]
# 设定模拟时间
time = Setup[2]
# 设定热导率
thermalConductivity = Setup[3]
# 设定比热容
specificHeatCapacity = Setup[4]
# 设定密度
density = Setup[5]
# 计算传热系数
alpha = thermalConductivity / (specificHeatCapacity * density)
# 计算时间点个数（循环次数）
timepoints = round(time / Microtime)

# 结构数组初始化
Structure = np.load('Structure.npy')
# 引导数组，产生遮罩，区分环境变量与本体变量，计算过程以此引导
Guide = guide(Structure)
# 初始温度分布
Tdistribution = np.load('Tdistribution.npy')

# 为优化性能引入的三个全零矩阵
Zeromat1 = zeromat(Tdistribution)
Zeromat2 = zeromat(Tdistribution)
Zeromat3 = zeromat(Tdistribution)

# 初始化结束
print('初始化结束\n开始计算，请稍候')

# 计算循环

for i in range(timepoints):
    # 计算温度的时间偏导数
    DirT = dirTot(
        Tdistribution, 
        Guide, 
        Zeromat1, 
        Zeromat2, 
        Zeromat3, 
        MicroDel, 
        alpha
        )
    # 计算温度变化差值
    DT = dT(DirT, Microtime)
    # 重新计算温度分布
    Tdistribution = np.array(Tdistribution) + np.array(DT)

# 结果输出
np.save('TdistributionRes.npy', Tdistribution)
np.save('Guide.npy', Guide)

# 计算结束
print('计算结束，结果已保存')
