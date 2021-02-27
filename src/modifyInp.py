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

# publicPath
publicPath = os.path.abspath(os.path.join(os.getcwd()))
# filename
inp_file_name = 'baseline.inp'
out_file_name = 'try-case.inp'
inp_file_path = os.path.join(publicPath,'static',inp_file_name)
out_file_path = os.path.join(publicPath,'mock','random', out_file_name)

#initialize a baseline model object
# baseline = swmmio.Model(path)
baseline = swmmio.core.inp(inp_file_path)
baselineModel = swmmio.Model(inp_file_path)
baselineLinks = baselineModel.links.dataframe
baselineNodes = baselineModel.nodes.dataframe
timeseries = baseline.timeseries
inflows = baseline.inflows

# nodes = baseline.nodes.dataframe
# links = baseline.links.dataframe


def setFlowOnAverage(scenario,startTime,endTime):
  '''
  description: set the flow evenly distributed over a specified period of time
  params :
    scenario:: [[pipe1, inflow1],[pipe2,inflow2],...]
    startTime:: string, start of the time to be modified, format:%m/%d/%Y %H:%M, e.g. 12/01/2020 0:00
    endTime:: string, end of the time to be modified, format:%m/%d/%Y %H:%M, e.g. 12/01/2020 0:00
    timeRange: [startTime,endTime)
  return :void
    modified inp will be saved as random.inp in static/random
  '''
  # timeseries = baseline.timeseries
  # parse startTime and endTime
  # 1. check if there's specified date
  try:
    test = time.mktime(time.strptime(timeseries['Time'][0],'%m/%d/%Y %H:%M'))
    SpecifyDate = True
  except:
    SpecifyDate = False
  # 2. calculate the timestamp
  startTime = parseTime(startTime)
  endTime = parseTime(endTime)
  
  # calculate the timeseries step(s)
  step1 = parseTime(timeseries['Time'][0])
  step2 = parseTime(timeseries['Time'][1])
  step = (step2-step1)
  # print(startTime, endTime, step)

  # 3. split the pipe RDII into both ends
  for i in range(0, len(scenario)):
    pipe = scenario[i][0]
    # inflow evenly distributed over a specified period of time
    averageFlow = scenario[i][1] / ((endTime-startTime) / step) / 2
    inletNode = baselineLinks.loc[pipe]['InletNode']
    outletNode = baselineLinks.loc[pipe]['OutletNode']
    inletNodeTimeSeries = inflows.loc[inletNode]['Time Series']
    inletNodeSfactor = inflows.loc[inletNode]['Sfactor']
    outletNodeTimeSeries = inflows.loc[outletNode]['Time Series']
    outletNodeSfactor = inflows.loc[outletNode]['Sfactor']
    
    nodes = [
      {'timeseries' : inletNodeTimeSeries, 'sfactor' : inletNodeSfactor},
      {'timeseries' : outletNodeTimeSeries, 'sfactor' : outletNodeSfactor}
    ]
    for node in nodes:
      # shallow copy
      curTimeSeries = timeseries.loc[node['timeseries']]
      # print(curTimeSeries)
      for j in range(len(curTimeSeries)):
        curTime = parseTime(curTimeSeries['Time'].iloc[j])
        # modify the timeseries within the range
        if curTime>=startTime and curTime<=endTime:
          originalFlow = float(curTimeSeries['Value'].iloc[j])
          # note: because of chained index, timeseries.loc[timeseriesIndex,'Value'][j] is just a copy of a slice from a DataFrame
          # any assignment won't affect the original DataFrame
          newFlow = averageFlow / node['sfactor']
          timeseries.loc[(timeseries['Time'] == curTimeSeries['Time'].iloc[j])&(timeseries.index == node['timeseries']),'Value'] = originalFlow + newFlow
  
  # save as random.inp in mock/random
  baseline.timeseries = timeseries
  if not os.path.exists(os.path.split(out_file_path)[0]):
    os.makedirs(os.path.split(out_file_path)[0])
  baseline.save(out_file_path)

# test this module
setFlowOnAverage([['1',250]],'0:00','12:00')
# print(timeseries.loc[['T1','T2']])
# try_case = swmmio.Model(os.path.join(publicPath,'static','random','try-case.inp'))

