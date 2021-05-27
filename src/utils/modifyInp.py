"""
modify data in inp file
"""
import os
import numpy as np
import swmmio
import sys
import pandas as pd
import time

# default configs
config = {
  'inp_file_name': 'jiangjiaba.inp',
  'out_file_name': 'try-case.inp',
  'publicPath': os.path.abspath(os.path.join(os.getcwd()))
}
config['inp_file_path'] = os.path.join(config['publicPath'], 'static', config['inp_file_name'])
config['out_file_path'] = os.path.join(config['publicPath'], 'mock', 'random', config['out_file_name'])

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
    description: parse string to timestamp, if there's no specified date, a default date '01/01/2000' will be added to the string
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

def formatTime(format,timestamp):
  """
    description: format timestamp to formatted string
  params :
    timestamp:: int
    format:: string : the format of the out time string
  return :
    ret::string
  """
  return time.strftime(format, time.localtime(timestamp))
class Inp:
  """
  read a inp file, take it as a baseline, make timeseries changes on that baseline and finally save a new inp file
  """

  def __init__(self,inp_file_path,out_file_path):
    if not inp_file_path:
      inp_file_path = config['inp_file_path']
    if not out_file_path:
      out_file_path = config['out_file_path']
    #initialize some baseline dataframes
    self.baseline = swmmio.core.inp(config['inp_file_path'])
    self.baselineModel = swmmio.Model(config['inp_file_path'])
    self.baselineLinks = self.baselineModel.links.dataframe
    self.baselineNodes = self.baselineModel.nodes.dataframe 
    self.timeseries = self.baseline.timeseries # any changes should be made on deep copy of self.timeseries
    # print(type(baselineNodes.iloc[0]['InvertElev'])) #numpy.float64

  def setFlowOnAverage(self,scenario,inp_file_path = config['inp_file_path'], out_file_path = config['out_file_path']):
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
    # 0. deep copy the timeseries dateframe
    timeseries = self.timeseries.copy(deep=True)
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
      inletNode = self.baselineLinks.loc[pipe]['InletNode']
      outletNode = self.baselineLinks.loc[pipe]['OutletNode']
      inletNodeTimeSeries = self.inflows.loc[inletNode]['Time Series']
      inletNodeSfactor = self.inflows.loc[inletNode]['Sfactor']
      try:
      # in case the outlet node is the outfall
        outletNodeTimeSeries = self.inflows.loc[outletNode]['Time Series']
        outletNodeSfactor = self.inflows.loc[outletNode]['Sfactor']
        inlet = {'newValue' : averageFlow / inletNodeSfactor * endBonus,
        'startTime': startTime, 'endTime': endTime}
        outlet = {'newValue' : averageFlow / outletNodeSfactor * endBonus,
        'startTime': startTime, 'endTime': endTime}
      except:
        # the outlet node is the outfall
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
      curTime = parseTime(timeseries.loc[i,'Time'])
      # timeseriesIndex: T1,T2,T3...
      timeseriesIndex = timeseries.index[i]
      node = nodes[timeseriesIndex]
      if curTime >= node['startTime'] and curTime < node['endTime']:
        timeseries.loc[i,'Value'] = float(timeseries.iloc[i,'Value']) + node['newValue']
    # save as random.inp in mock/random
    self.baseline.timeseries = timeseries
    if not os.path.exists(os.path.split(out_file_path)[0]):
      os.makedirs(os.path.split(out_file_path)[0])
    self.baseline.save(out_file_path)

  def setTimeseries(
    self,
    values,
    time_list,
    nodes_name,
    out_file_path = config['out_file_path']
  ):
    """
    Transfer flat values list into timeseries DataFrame and append it into the new inp file

    Parameters
    ----------
      values:: [<float>] : the flatten values of  timeseries
      time_list:: [<timestamp::float>] the time of timeseries.
      nodes_name:: [<string>] the name of nodes
      out_file_path:: the absolute path where a new inp file will be saved
      
    Returns
    ----------
    void
    a new inp file will be saved
    """
    # 0. deep copy the timeseries dateframe
    timeseries = self.timeseries.copy(deep=True)

    # 1. convert the input data into inp DataFrame
    timeseries_name_column = []
    date_column = []
    time_column = []
    value_column = values
    # cover the node name to the corresponding time series name
    for node_name in nodes_name:
      timeseries_name_column.append([self.inflows.loc[node_name,'Time Series']] * len(time_list))
    # calculate the date_column and the time_column from time_list
    for _ in time_list:
      date_column.append(formatTime('%m/%d/%Y',_))
      time_column.append(formatTime(' %H:%M',_))
    # fill the date_column and time_column for every timeseries name
    date_column = [date_column] * len(nodes_name)
    time_column = [time_column] * len(nodes_name)
    # a temp dict
    tmp = {
      'Name': timeseries_name_column,
      'Date': date_column,
      'Time': time_column,
      'Value': value_column
    }
    # convert the tmp to DataFrame
    new_timeseries = pd.DataFrame(tmp)

    # 3. append the new timeseries to the old
    self.baseline.timeseries = pd.concat([self.timeseries, new_timeseries],axis = 0, ignore_index=True)

    # 4. save a new inp file
    if not os.path.exists(os.path.split(out_file_path)[0]):
      # make directory if it doesn't exist
      os.makedirs(os.path.split(out_file_path)[0])
    if os.path.exists(out_file_path):
      # delete the existing inp file
      os.remove(out_file_path)
    # save a new inp file
    self.baseline.save(out_file_path)

if __name__ == '__main__':
  """
  test this module
  """
  # setFlowOnAverage([['1',250]],'0:00','12:00')
  # print(timeseries.loc[['T1','T2']])
  # try_case = swmmio.Model(os.path.join(publicPath,'static','random','try-case.inp'))

  baseline = swmmio.core.inp(config['inp_file_path'])
  baselineModel = swmmio.Model(config['inp_file_path'])
  baselineLinks = baselineModel.links.dataframe
  baselineNodes = baselineModel.nodes.dataframe
  timeseries = baseline.timeseries
  print()