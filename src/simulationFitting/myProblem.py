# -*- coding: utf-8 -*-
import numpy as np
# import pandas as pd
import geatpy as ea
import pandas as pd
# from geatpy.Problem import Problem
# from swmm5.swmm5tools import SWMM5Simulation
import sys
from sys import path
import os

config = {
  'publicPath': os.path.abspath(os.path.join(os.getcwd())),
}
path.append(config['publicPath'])

from src.utils.modifyInp import Inp
from src.utils.runSwmm5 import runSimulation
from src.utils.NashSutcliffe import calculateNashSutcliffe

# def read_data(infile,gauge_index):
#   gauge_dict = ('J13','J36','J57','P64')
#   df1 = pd.read_excel(infile)
#   res = list(df1[gauge_dict[gauge_index]])[1::]
#   return (res,sum(res)/len(res))

# def get_result(inpfile):
#   st1 = SWMM5Simulation(inpfile)
#   return st1


class MyProblem(ea.Problem):  # 继承Problem父类
    # 自定义问题类
    def __init__(self, M, dataPath):
        """
        M:: int -- 目标维数
        dataPath: 包含一次拟合所需要的数据所在的路径，其中：
          baseline.xlsx -> baseline:: [baseline1[<float>],baseline2[<float>],...] -- 预先设定的基础值
          nodes_name.xlsx -> nodes_name :: list<str> -- 要修改的节点名称
          baseline.xlsx -> time_list:: [<timestamp::float>] -- the time of timeseries.
          objData.xlsx -> ObjData :: [obj1[<float>],obj2[<float>],...] -- 要拟合的目标值
          try-case.inp -> 作为种群个体的测试管网
        """
        """
        1. 初始化信息
        """
        self.dataPath = dataPath
        # baseline of values
        baseline_df = pd.read_excel(os.path.join(self.dataPath, 'baseline.xlsx'))
        # nodes neet to be modified
        nodes_name_df = pd.read_excel(os.path.join(self.dataPath, 'nodes_name.xlsx'),sheet_name = 'input')
        """
        模型输入信息
        """
        self.nodes_name = nodes_name_df['nodes_name']
        self.time_list = baseline_df['TimeStamp']
        baseline = baseline_df['Baseline']
        # 展开baseline得到values
        self.values = []
        for _ in baseline:
            self.values.append(_)
        """
        模型输出信息
        """
        simulation_info_df = pd.read_excel(os.path.join(self.dataPath, 'nodes_name.xlsx'),sheet_name = 'output')
        # 模型输出节点类型(详见src/utils/runSwmm5.py注释)
        self.structure = list(simulation_info_df['Structure'])
        # 模型输出节点编号(详见src/utils/runSwmm5.py注释)
        self.index = list(simulation_info_df['index'])
        # 模型输出数据类型(详见src/utils/runSwmm5.py注释)
        self.resultType = list(simulation_info_df['ResultType'])
 
        """
        2.初始化遗传算法问题参数
        """
        name = 'MyProblem'  # 初始化name（函数名称，可以随意设置）
        self.M = M  # 初始化M（目标维数）
        self.maxormins = [1] * M  # 初始化maxormins（目标最小最大化标记列表，1：最小化该目标；-1：最大化该目标）
        Dim = len(self.values)  # 初始化Dim（决策变量维数）
        varTypes = [0] * Dim  # 初始化varTypes（决策变量的类型，0：实数；1：整数）
        lb = [0.5 * _ for _ in self.values] # 决策变量下界
        ub = [1.5 * _ for _ in self.values]  # 决策变量上界
        lbin = [1] * Dim  # 决策变量下边界是否包含
        ubin = [1] * Dim  # 决策变量上边界是否包含
        self.objData = pd.read_excel(os.path.join(self.dataPath, 'objData.xlsx'))['objData']
        # 调用父类构造方法完成实例化
        ea.Problem.__init__(self, name, self.M, self.maxormins, Dim, varTypes,
                            lb, ub, lbin, ubin)
        """
        3. 初始化modifyInp类，读取baseline inp
        """
        self.inp = Inp(inp_file_path = os.path.join(config['publicPath'], 'static', 'baseline.inp'),
                       out_file_path = os.path.join(self.dataPath,'try-case.inp'))

    def aimFunc(self, pop):  # 目标函数
        """
        1. 获取决策变量矩阵Vars和适应度向量f
        """
        Vars = pop.Phen  # 得到决策变量矩阵
        f = np.zeros(shape=(len(Vars), 1))
        """
        2. 计算适应度向量f
        """
        for i, v in enumerate(Vars):
            # i为第i个个体, v为染色体
            """
            2.1 修改timeseries并保存inp文件
            """
            self.inp.setTimeseries(values = v,
                                   time_list = self.time_list,
                                   nodes_name = self.nodes_name,
                                   out_file_path = '')
            """
            2.2 运行模型获取结果
            """
            # try:
            runSimulation(self.structure, self.index, self.resultType,
                          os.path.join(self.dataPath,'try-case.inp'),
                          os.path.join(self.dataPath,'try-case.xlsx'))

            f[i] = calculateNashSutcliffe(observed_data_path = os.path.join(self.dataPath, 'objData.xlsx'), 
                                          simulated_data_path = os.path.join(self.dataPath,'try-case.xlsx'))
            # except:
            #     f[i] = 0  # swmm5包有时候会出现error 303 无法读取，如果出现这个错，就全赋值0，让这个个体淘汰掉好了
        pop.ObjV = f  # 把求得的目标函数值赋值给种群pop的ObjV

        # def calReferObjV(self):  # 计算全局最优解
        #     uniformPoint, ans = ea.crtup(self.M, 10000)  # 生成10000个在各目标的单位维度上均匀分布的参考点
        #     globalBestObjV = uniformPoint / 2
        #     return globalBestObjV
    def modifyInpMannually(self,values,out_file_path):
      """
      手动保存case
      """
      self.inp.setTimeseries(values = values,
                             time_list = self.time_list,
                             nodes_name = self.nodes_name,
                             out_file_path = out_file_path)

# if __name__ == '__main__':
#     #
#     #
#     # read_data('监测点数据.xlsx',1)
#
#     get_result('case_empty.inp')
