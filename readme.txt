----------------------------------------------------------------
*************************** 使用说明 ****************************
第三方库：numpy; matplotlib; seaborn
在 setup.txt 文件中写入脚本，半角分号分割元素
1.写入格式：（不要换行！！！！！）
    空间微元尺寸(m);
    时间微元长度(s);
    仿真时间(s);
    物体导热率(W/(K*m^2));
    比热容(J/(K*kg));
    密度(kg/m^3)

2.仿真形状设置：
    在 shapeGenerate.py 中生成结构数组 structure.npy，温度分布数组 
Tdistribution.npy 默认脚本是绘制实心圆的程序，请自行仿照书写，随后使
用setup.py进行操作。结构数组中：0表示虚无，1表示边界，2表示模拟的微元。

3.运行模拟：
    打开 main.py 并运行，随后系统会主动调用 3D.py 进行传热的PDE计算，
使用 structure.npy 与 Tdistribution.npy 作为参数计算温度分布并获得
温度分布结果 TdistributionRes.npy 与引导矩阵结果（本体数值 = 1,非本
体数值 = 0）Guide.npy 。
    随后 main.py 会调用 visualization.py 进行数据可视化输出，该程序
会调用 TdistributionRes.npy 与 Guide.npy 进行数据加工，输出某个截面
的温度分布，以热图的形式展现，具体信息在对应程序中配置。

4.结果
最后的结果会以图片形式展示模拟物体（示例程序为球体）各个截面温度分布
并保存为 Result.tif
-----------------------------------------------------------------
注：千万不要给所有文件重命名 ，保存文本使用UTF-8格式，半角符号
*************************** 介绍结束 *****************************
