import os
import pandas as pd
import time
from swmm5.swmm5tools import SWMM5Simulation
from .inpOptions import configInp
# some configs
config = {
  'publicPath': os.path.abspath(os.path.join(os.getcwd())),
  'observed_data': 'observed_date.csv',
  'simulated_data': 'simulated_data.csv',
}
config['inp_file_path'] = os.path.join(config['publicPath'], 'mock', 'random', 'try-case.inp')
config['out_file_path'] = os.path.join(config['publicPath'], 'mock', 'random', 'result.csv')

NODE_RESULT_TYPE = ['LEVEL(m)','Hydraulic head(m)','Volume of stored + ponded water(m3)', 
                    'Lateral inflow (LPS)', 'Total inflow(LPS)', 'Flow lost to flooding(LPS)', 
                    'Concentration(mg/l)']
LINK_RESULT_TYPE = ['Flow rate(LPS)', 'Flow depth(m)', 'Flow velocity(m/s)',
                    'Froude number', 'Capacity', 'Concentration(mg/l)']

def runSimulation(structure, index, resultType, inp_file_path, out_file_path):
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
    the  output file will be like:
    INDEX   VALUE   TIME   DATE         TYPE
    1       1.324   00:30  01/01/2020   LEVEL(m)
    2       1.484   01:00  02/01/2020   LEVEL(m)
    ...
    1       0.482   00:30  01/01/2020   FLOW(LPS)
    ...
  
  :return: <generator object SWMM5Simulation.Results at 0x00000207600ED660>
  :output: generate the result.csv to save the result if the output path specified
  '''
  # preprocess the params
  structure, index, resultType
  if not isinstance(structure, list):
    structure = [structure]
  if not isinstance(index, list):
    index = [index]
  if not isinstance(resultType, list):
    resultType = [resultType]
  # run the simulation
  st = SWMM5Simulation(inp_file_path)
  # validate the params
  if len(structure) != len(index) or len(structure) != len(resultType):
      raise Exception('length of structure and index don\'t match')
      return st
  # if need to generate result.csv
  if out_file_path:
    if not os.path.exists(os.path.split(out_file_path)[0]):
      os.makedirs(os.path.split(out_file_path)[0])
    # some setting infos
    infoDict = configInp(inp_file_path,'',options=['REPORT_START_DATE', 'REPORT_START_TIME', 'END_DATE', 'END_TIME'],values=[])
    step = st.SWMM_ReportStep # the report time step of the unit:min
    reportStartDate = infoDict['REPORT_START_DATE']
    reportStartTime = infoDict['REPORT_START_TIME']
    endDate = infoDict['END_DATE']
    endTime = infoDict['END_TIME']
    reportStartTimeStamp = time.mktime(time.strptime(reportStartDate+' '+reportStartTime,'%m/%d/%Y %H:%M:%S'))
    endTimeStamp = time.mktime(time.strptime(endDate+' '+endTime,'%m/%d/%Y %H:%M:%S'))
    # dict that save the result
    result = {
      'INDEX': [],
      'VALUE': [],
      'TIME': [],
      'DATE': [],
      'TYPE': []
    }
    # for every structure
    for i in range(len(structure)):
      if structure[i] == 'NODE':
        vals = list(st.Results('NODE', str(index[i]), resultType[i]))
        result['VALUE'] += vals
        curTimeStamp = 0
        for j in range(len(vals)):
          curTimeStamp = reportStartTimeStamp + 30 * 60 * 1000 * i
          result['INDEX'].append(index[i])
          result['TIME'].append(time.strftime('%H:%M:%S', time.localtime(curTimeStamp)))
          result['DATE'].append(time.strftime('%m/%d/%Y', time.localtime(curTimeStamp)))
          result['TYPE'].append(NODE_RESULT_TYPE[resultType[i]])
      elif structure[i] == 'LINK':
        vals = list(st.Results('LINK', str(index[i]), resultType[i]))
        result['VALUE'] += vals
        curTimeStamp = 0
        for j in range(len(vals)):
          curTimeStamp = reportStartTimeStamp + 30 * 60 * 1000 * i
          result['INDEX'].append(index[i])
          result['TIME'].append(time.strftime('%H:%M:%S', time.localtime(curTimeStamp)))
          result['DATE'].append(time.strftime('%m/%d/%Y', time.localtime(curTimeStamp)))
          result['TYPE'].append(LINK_RESULT_TYPE[resultType[i]])
      elif structure[i] == 'SUBCATCH':
        # TODOS
        pass
      elif structure[i] == 'SYS':
        # TODOS
        pass
      else:
        # REMAIN
        pass
    df = pd.DataFrame(result)
    # index = 0 means no index column
    df.to_csv(out_file_path,index = 0)
  # finally, return the st object
  return st

if __name__ == '__main__':
  # st = SWMM5Simulation(inp_file_path)
  # print(st.Results('NODE','1',4))
  runSimulation(['NODE','LINK'],['1','4'],[0,0])
