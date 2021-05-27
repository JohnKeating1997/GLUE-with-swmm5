'''
Author: your name
Date: 2021-05-26 20:26:55
LastEditTime: 2021-05-26 20:29:19
LastEditors: Please set LastEditors
Description: In User Settings Edit
FilePath: \GLUE-with-swmm5\src\simulationFitting\main.py
'''
from src.utils.modifyInp import setFlowOnAverage
from src.utils.runSwmm5 import runSimulation
from src.utils.NashSutcliffe import calculateNashSutcliffe
import geatpy as ea
from src.simulationFitting.myProblem import MyProblem as MyProblem

