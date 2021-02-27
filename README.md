# GLUE-with-swmm5
Generalized Likelihood Uncertainty Estimation based on Swmm5 Simulation

package:
pyswmm
swmmio

example-case.inp
informal RDII:
  conduit 37 : 48LPS (distributed evenly between 0:00-5:30)
  conduit 53 : 36LPS (distributed evenly between 3:00-8:30)

STAGE1:
  已知RDII在某段时间内的值，然后在空间上将RDII值分配到各个管段i上（再均分到i两端的节点上），时间上暂时采用均分的方式(TODOS:后期根据监测数据的波动情况提供prior distribution)
  经过GLUE分析5000次后，重复5000次模拟得到各个管段RDII值的方差和均值，可以得到一个正态分布的概率密度函数PDF