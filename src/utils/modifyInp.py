import os
import numpy as np
import swmmio
import sys
import pandas as pd
import time

def pandasDisplaySetup():
  #pandas设置最大显示行和列
  pd.set_option('display.max_columns',50)
  pd.set_option('display.max_rows',300)
  
  #调整显示宽度，以便整行显示
  pd.set_option('display.width',1000) 
  
  #显示所有列
  pd.set_option('display.max_columns', None)
  #显示所有行
  pd.set_option('display.max_rows', None)
  #设置value的显示长度为100，默认为50
  pd.set_option('max_colwidth',100)

pandasDisplaySetup()

def parseTime(string):
  """
    description: parse string to time tuple, if there's no specified date, an informal date '01/01/2000' will be added to the string
  params :
    string: the input time string
  return :
    ret: timestamp

  """
  try:
    ret = time.mktime(time.strptime(string,'%m/%d/%Y %H:%M'))
  except:
    # add an informal date '01/01/2000' so that startTime and startTime can be parsed into timestamp
    ret = time.mktime(time.strptime('01/01/2000 '+str(string),'%m/%d/%Y %H:%M'))
  return ret

# configs
config = {
  'inp_file_name': 'baseline.inp',
  'out_file_name': 'try-case.inp',
  'publicPath': os.path.abspath(os.path.join(os.getcwd()))
}
config['inp_file_path'] = os.path.join(config['publicPath'], 'static', config['inp_file_name'])
config['out_file_path'] = os.path.join(config['publicPath'], 'mock', 'random', config['out_file_name'])

#initialize some baseline dataframes
baseline = swmmio.core.inp(config['inp_file_path'])
baselineModel = swmmio.Model(config['inp_file_path'])
baselineLinks = baselineModel.links.dataframe
baselineNodes = baselineModel.nodes.dataframe

timeseries = baseline.timeseries

config['timeColumnIndex'] = list(baseline.timeseries.columns).index('Time')
config['valueColumnIndex'] = list(baseline.timeseries.columns).index('Value')

inflows = baseline.inflows
# print(type(baselineNodes.iloc[0]['InvertElev'])) #numpy.float64

def setFlowOnAverage(scenario,inp_file_path = config['inp_file_path'], out_file_path = config['out_file_path']):
  '''
  description: set the flow evenly distributed over a specified period of time
  params :
    scenario: [[pipe1 <string>, inflow1 <float>, startTime1: <string>, endTime1: <string>],
               [pipe2 <string>,inflow2 <float>, startTime2: <string>, endTime2: <string>],...]
              note: the time format is expected to be like the following:
                format:%m/%d/%Y %H:%M, e.g. 12/01/2020 0:00
              if the date is not be specified, that is ok.
    timeRange: [startTime,endTime)
  return :void
    modified inp will be saved as random.inp in static/random
  '''
  # parse startTime and endTime
  # 1. check if there's specified date
  try:
    test = time.mktime(time.strptime(timeseries['Time'][0],'%m/%d/%Y %H:%M'))
    SpecifyDate = True
  except:
    SpecifyDate = False

  # 2. calculate the timeseries step(s)
  step1 = parseTime(timeseries['Time'][0])
  step2 = parseTime(timeseries['Time'][1])
  step = (step2-step1)
  # print(startTime, endTime, step)

  # 3. split the pipe RDII into both ends
  nodes = {}
  for i in range(0, len(scenario)):
    # endBonus is to handle the outlet node is the outfall
    endBonus = 1
    pipe = scenario[i][0]
    # inflow evenly distributed over a specified period of time
    startTime = parseTime(scenario[i][2])
    endTime = parseTime(scenario[i][3])
    averageFlow = scenario[i][1] / ((endTime-startTime) / step) / 2
    inletNode = baselineLinks.loc[pipe]['InletNode']
    outletNode = baselineLinks.loc[pipe]['OutletNode']
    inletNodeTimeSeries = inflows.loc[inletNode]['Time Series']
    inletNodeSfactor = inflows.loc[inletNode]['Sfactor']
    # in case the outlet node is the outfall
    try:
      outletNodeTimeSeries = inflows.loc[outletNode]['Time Series']
      outletNodeSfactor = inflows.loc[outletNode]['Sfactor']
      inlet = {'newValue' : averageFlow / inletNodeSfactor * endBonus,
      'startTime': startTime, 'endTime': endTime}
      outlet = {'newValue' : averageFlow / outletNodeSfactor * endBonus,
      'startTime': startTime, 'endTime': endTime}
    except:
      endBonus = 2
      inlet = {'newValue' : averageFlow / inletNodeSfactor * endBonus,
      'startTime': startTime, 'endTime': endTime}
      outlet = None
    if inletNodeTimeSeries in nodes.keys():
      # TODOS: assume the pipes share the same RDII time mode
      nodes[inletNodeTimeSeries]['newValue'] += inlet['newValue'] 
    else:
      nodes[inletNodeTimeSeries] = inlet
    if outlet is not None:
      if outletNodeTimeSeries in nodes.keys():
        nodes[outletNodeTimeSeries]['newValue'] += outlet['newValue'] 
      else:
        nodes[outletNodeTimeSeries] = outlet
    # for node in nodes:
    #   # shallow copy
    #   curTimeSeries = timeseries.loc[node['timeseries']]
    #   # print(curTimeSeries)
    #   for j in range(len(curTimeSeries)):
    #     curTime = parseTime(curTimeSeries['Time'].iloc[j])
    #     # modify the timeseries within the range
    #     if curTime >= startTime and curTime <= endTime:
    #       originalFlow = float(curTimeSeries['Value'].iloc[j])
    #       # note: because of chained index, timeseries.loc[timeseriesIndex,'Value'][j] is just a copy of a slice from a DataFrame
    #       # any assignment won't affect the original DataFrame
    #       newFlow = averageFlow / node['sfactor'] * endBonus
    #       timeseries.loc[(timeseries['Time'] == curTimeSeries['Time'].iloc[j])&(timeseries.index == node['timeseries']),'Value'] = originalFlow + newFlow
    #     elif curTime > endTime:
    #       break
  # traverse the timeseries dataframe (very time consuming)
  for i in range(len(timeseries)):
    curTime = parseTime(timeseries.iloc[i,config['timeColumnIndex']])
    timeseriesIndex = timeseries.index[i]
    node = nodes[timeseriesIndex]
    if curTime >= node['startTime'] and curTime < node['endTime']:
      timeseries.iloc[i,config['valueColumnIndex']] = float(timeseries.iloc[i,config['valueColumnIndex']]) + node['newValue']
  # save as random.inp in mock/random
  baseline.timeseries = timeseries
  if not os.path.exists(os.path.split(out_file_path)[0]):
    os.makedirs(os.path.split(out_file_path)[0])
  baseline.save(out_file_path)

if __name__ == '__main__':
  # test this module
  setFlowOnAverage([['1',250]],'0:00','12:00')
  # print(timeseries.loc[['T1','T2']])
  # try_case = swmmio.Model(os.path.join(publicPath,'static','random','try-case.inp'))

