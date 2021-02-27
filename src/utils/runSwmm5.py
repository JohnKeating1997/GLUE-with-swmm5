import os
import pandas as pd
from swmm5.swmm5tools import SWMM5Simulation
# publicPath
publicPath = os.path.abspath(os.path.join(os.getcwd()))
inp_file_path = os.path.join(publicPath, 'mock', 'random', 'try-case.inp')
out_file_path = os.path.join(publicPath, 'mock', 'random', 'result.xlsx')


def runSimulation(structure, index, type, inp_file_path=inp_file_path,
                  out_file_path=out_file_path):
    '''
    description: run a swmm5 simulation
    :param structure: <[string] | string> type of structure,such as 'SUBCATCH', 'NODE', 'LINK', 'SYS'
    :param index: <[string] | string> index of specified structure of which the result will be written into xxx.csv
    :param inp_file_path: <string> absolute path of inp file
    :param out_file_path: <string> absolute path of output file
    
    :return: void
      generate a csv file to save the result
    '''
  st = SWMM5Simulation(inp_file_path)
  # some configs
  step = st.SWMM_ReportStep # unit:min

  
  # dict that save the result of flow
  flowResult = {
    'date': [],
    'time': []
  }
  # dict that save the result of water level
  levelResult = {
    'date': [],
    'time': []
  }
  print(st.Results('NODE','1',4))
  # multiple structures
  if isinstance(structure,list) and isinstance(index,list):
    if len(structure)!=len(index):
      print('length of structure and index don\'t match')
      return
    for i in range(len(structure)):

# mock
st = SWMM5Simulation(inp_file_path)
print(st.Results('NODE','1',4))
