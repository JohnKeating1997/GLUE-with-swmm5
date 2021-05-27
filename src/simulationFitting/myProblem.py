# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import geatpy as ea
# from geatpy.Problem import Problem
from swmm5.swmm5tools import SWMM5Simulation
from src.utils.modifyInp import Inp
from src.utils.runSwmm5 import runSimulation
from src.utils.NashSutcliffe import calculateNashSutcliffe
import os

config = {
  'inp_file_name': 'jiangjiaba.inp',
  'out_file_name': 'try-case.inp',
  'publicPath': os.path.abspath(os.path.join(os.getcwd()))
}
config['inp_file_path'] = os.path.join(config['publicPath'], 'static', config['inp_file_name'])
config['out_file_path'] = os.path.join(config['publicPath'], 'mock', 'random', config['out_file_name'])

# 自定义问题类
def read_data(infile,gauge_index):
    gauge_dict = ('J13','J36','J57','P64')
    df1 = pd.read_excel(infile)
    res = list(df1[gauge_dict[gauge_index]])[1::]
    return (res,sum(res)/len(res))

def get_result(inpfile):
    st1 = SWMM5Simulation(inpfile)
    return st1

class MyProblem(ea.Problem):  # 继承Problem父类
    def __init__(self, M, baseline, time_list, nodes_name, ObjData):
        """
        M:: int -- 目标维数
        baseline:: [baseline1[<float>],baseline2[<float>],...] -- 预先设定的基础值
        nodes_name :: list<str> -- 要修改的节点名称
        time_list:: [<timestamp::float>] -- the time of timeseries.
        ObjData :: [obj1[<float>],obj2[<float>],...] -- 要拟合的目标值
        """
        """
        1. 初始化信息
        """
        self.nodes_name = nodes_name
        self.time_list = time_list
        # 展开baseline得到values
        self.values = []
        for _ in baseline:
          self.values += _
        """
        2.初始化问题参数
        """
        name = 'MyProblem'  # 初始化name（函数名称，可以随意设置）
        self.M = M  # 初始化M（目标维数）
        self.maxormins = [1] * M  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        Dim = len(self.values)  # 初始化Dim（决策变量维数）
        varTypes = [0] * Dim  # 初始化varTypes（决策变量的类型，0：实数；1：整数）
        lb = self.values * 0.5  # 决策变量下界
        ub = self.values * 1.5  # 决策变量上界
        lbin = [1] * Dim  # 决策变量下边界是否包含
        ubin = [1] * Dim  # 决策变量上边界是否包含
        self.ObjData = ObjData # 要拟合的目标值
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, self.M, self.maxormins, Dim, varTypes, lb, ub, lbin, ubin)
        """
        3. 初始化modifyInp类，读取baseline inp
        """
        self.inp = Inp(inp_file_path = config['inp_file_path'], out_file_path = config['out_file_path'])

    def aimFunc(self, pop):  # 目标函数
        """
        1. 获取决策变量矩阵Vars和适应度向量f
        """
        Vars = pop.Phen  # 得到决策变量矩阵
        f = np.zeros(shape=(len(Vars),1))
        """
        2. 计算适应度向量f
        """
        for i,v in enumerate(Vars):
          # i为第i个个体, v为染色体
            """
            2.1 修改timeseries并保存inp文件
            """
            self.inp.setTimeseries(values = v, time_list = self.time_list, nodes_name = self.nodes_name)
            """
            获取结果
            """
            try:
                st = get_result(inpfile='case_try.inp')
                
            except:
                res = list(np.zeros(len(self.objData)))   ## swmm5包有时候会出现error 303 无法读取，如果出现这个错，就全赋值0，让这个个体淘汰掉好了

            MSE = 0
            for j in range(len(self.ObjData)):
                MSE += (self.ObjData[j]-res[j])**2
            RMSE = np.sqrt(MSE/len(self.ObjData))
            f[i] = RMSE
        pop.ObjV = f  # 把求得的目标函数值赋值给种群pop的ObjV




    # def calReferObjV(self):  # 计算全局最优解
    #     uniformPoint, ans = ea.crtup(self.M, 10000)  # 生成10000个在各目标的单位维度上均匀分布的参考点
    #     globalBestObjV = uniformPoint / 2
    #     return globalBestObjV

# if __name__ == '__main__':
#     #
#     #
#     # read_data('监测点数据.xlsx',1)
#
#     get_result('case_empty.inp')
