'''
Author: your name
Date: 2021-05-26 20:26:55
LastEditTime: 2021-05-26 20:29:19
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \GLUE-with-swmm5\src\simulationFitting\main.py
'''
import numpy as np
import pandas as pd
import geatpy as ea
import sys
from sys import path
import os

config = {
  'publicPath': os.path.abspath(os.path.join(os.getcwd())),
}
path.append(config['publicPath'])

from src.simulationFitting.myProblem import MyProblem

if __name__ == '__main__':
    """
    0. define a problem
    """
    config['dataPath'] = os.path.join(config['publicPath'], 'mock', '20210529')
    # 目标变量维数
    M = 1
    problem = MyProblem(M, config['dataPath'])
    Encoding = 'BG'       # 编码方式
    NIND = 120            # 种群规模
    Field = ea.crtfld(Encoding, problem.varTypes, problem.ranges, problem.borders) # 创建区域描述器
    population = ea.Population(Encoding, Field, NIND) # 实例化种群对象（此时种群还没被初始化，仅仅是完成种群对象的实例化）
    """===============================算法参数设置============================="""
    myAlgorithm = ea.soea_SEGA_templet(problem, population)  # 实例化一个算法模板对象
    myAlgorithm.MAXGEN = 10  # 最大进化代数
    """
    1. 调用算法模板进行种群进化
    """
    [population, obj_trace, var_trace] = myAlgorithm.run()  # 执行算法模板
    population.save()  # 把最后一代种群的信息保存到文件中

    # 输出结果
    best_gen = np.argmin(problem.maxormins * obj_trace[:, 1]) # 记录最优种群个体是在哪一代
    best_ObjV = obj_trace[best_gen, 1]
    print('最优的目标函数值为：%s'%(best_ObjV))
    """
    2. 保存最优解
    """
    problem.modifyInpMannually(values = var_trace[best_gen], out_file_path = os.path.join(config['dataPath'],'best-case.inp'))
    # print('最优的控制变量值为：')
    # for i in range(var_trace.shape[1]):
    #     print(var_trace[best_gen, i])
    print('有效进化代数：%s'%(obj_trace.shape[0]))
    print('最优的一代是第 %s 代'%(best_gen + 1))
    print('评价次数：%s'%(myAlgorithm.evalsNum))
    print('时间已过 %s 秒'%(myAlgorithm.passTime))