import os
import numpy as np
import swmmio

# publicPath
publicPath = os.path.abspath(os.path.join(os.getcwd()))
path = publicPath + '\\static\\result.inp'
mymodel = swmmio.Model(path)
nodes = mymodel.nodes.dataframe
print(nodes)

# print(os.getcwd())
# def modify_inp(self,infile,pattern,output_name='case_try.inp'):
#     """
#     :param infile: 原inp文件
#     :param pattern: 各个上游节点24小时的流量输入，数组
#     :return: void，最后生成一个新inp文件,默认值"case_try.inp"
#     """
#     """
#     修改inp文件，最后生成新的inp文件，默认值"case_try.inp"
#     """
#     var = []
#     # 要插入的内容
#     tmp = ""
#     for inx in range(len(pattern)):
#         tmp += (str(np.around(pattern[inx], decimals=3)) + "  ")
#         if (inx+1) % 24 == 0 and (inx+1) != 1:
#             var.append(tmp)
#             tmp = ""

#     with open(infile, 'r')as inp:
#         lines = inp.readlines()
#         inflow_index = -1
#         pattern_index = -1
#         """
#         找到inflows 和 pattern的插入位置
#         """
#         for i, v in enumerate(lines):
#             if v == '[INFLOWS]\n':
#                 inflow_index = i + 3  # swmm5 文件有一些注释，所以要跳过两行
#             if v == '[PATTERNS]\n':
#                 pattern_index = i + 4
#             if inflow_index != -1 and pattern_index != -1:
#                 break

#         for i in range(len(self.nodes)):
#             flow_info = str(self.nodes[i]) + '                FLOW             ""               FLOW     1.0      1.0      ' + str(
#                 self.avg) + '      Pattern' + str(self.nodes[i]) + '\n'
#             lines.insert(inflow_index, flow_info)
#             inflow_index += 1

#             pattern_info = 'Pattern' + str(self.nodes[i]) + '         HOURLY     ' + var[i] + '\n'
#             lines.insert(pattern_index, pattern_info)
#             pattern_index += 1
#     """
#     生成新文件
#     """
#     if (os.path.exists(output_name)):
#         os.remove(output_name)
#     with open(output_name, 'w') as output:
#         output.writelines(lines)