import os
import pandas as pd
from swmm5.swmm5tools import SWMM5Simulation
# publicPath
publicPath = os.path.abspath(os.path.join(os.getcwd()))
inp_file_path = os.path.join(publicPath, 'mock', 'random', 'try-case.inp')
out_file_path = os.path.join(publicPath, 'mock', 'random', 'result.csv')


def runSimulation(structure, index, type, inp_file_path=inp_file_path,
                  out_file_path=out_file_path):
  '''
  description: run a swmm5 simulation
  :param structure: <[string] | string> type of structure,such as 'SUBCATCH', 'NODE', 'LINK', 'SYS'
  :param index: <[string] | string> index of specified structure of which the result will be written into result.csv
  :param resultType <[int] | int> type of the  result data
    NOTE: the following document from https://pypi.org/project/SWMM5/
    for 'SUBCATCH':
      0 Rainfall (in/hr or mm/hr)
      1 Snow depth (in or mm)
      2 Evaporation loss (in/hr or mm/hr)
      3 Infiltration loss (in/hr or mm/hr)
      4 Runoff rate (flow units)
      5 Groundwater outflow rate (flow units)
      6 Groundwater water table elevation (ft or m)
      7 Soil Moisture (volumetric fraction, less or equal tosoil porosity)
      8 Runoff concentration of TSS (mg/l)
    for 'NODE':
      0 Depth of water above invert (ft or m)
      1 Hydraulic head (ft or m)
      2 Volume of stored + ponded water (ft3 or m3)
      3 Lateral inflow (flow units)
      4 Total inflow (lateral + upstream) (flow units)
      5 Flow lost to flooding (flow units)
      6 Concentration of TSS (mg/l)
    for 'LINK':
      0 Flow rate (flow units)
      1 Flow depth (ft or m)
      2 Flow velocity (ft/s or m/s)
      3 Froude number
      4 Capacity (fraction of conduit filled)
      5 Concentration of TSS (mg/l)
    for 'SYS':
      0 Air temperature (deg. F or deg. C)
      1 Rainfall (in/hr or mm/hr)
      2 Snow depth (in or mm)
      3 Evaporation + infiltration loss rate (in/hr or mm/hr)
      4 Runoff flow (flow units)
      5 Dry weather inflow (flow units)
      6 Groundwater inflow (flow units)
      7 RDII inflow (flow units)
      8 User supplied direct inflow (flow units)
      9 Total lateral inflow (sum of variables 4 to 8) (flow units)
      10 Flow lost to flooding (flow units)
      11 Flow leaving through outfalls (flow units)
      12 Volume of stored water (ft3 or m3)
      13 Evaporation rate (in/day or mm/day)
  :param inp_file_path: <string> absolute path of inp file
  :param out_file_path: <string> absolute path of output file
  
  :return: <generator object SWMM5Simulation.Results at 0x00000207600ED660>
  :output: generate the result.csv to save the result if the output path specified
  '''
  # run the simulation
  st = SWMM5Simulation(inp_file_path)
  print(type(st))
  exit(0)
  # some configs
  step = st.SWMM_ReportStep # unit:min

  # dict that save the result
  flowResult = {
    'TIME': [],
    'FLOW': [],
    'TYPE': [],
    'UNIT': []
  }
  print(st.Results('NODE','1',4))
  # multiple structures
  if isinstance(structure,list) and isinstance(index,list):
    if len(structure)!=len(index):
      print('length of structure and index don\'t match')
      return
    for i in range(len(structure)):
      if structure[i] == 'NODE':
        pass
      elif structure[i] == 'LINK':
        pass
      elif structure[i] == 'SUBCATCH':
        pass
      elif structure[i] == 'SYS':
        pass
      else:
        pass
  elif (not isinstance(structure,list)) and (not isinstance(index,list)):
    pass
  else:
    raise Exception('length of structure and index don\'t match')
    return

if __name__ == '__main__':
  st = SWMM5Simulation(inp_file_path)
  print(st.Results('NODE','1',4))
