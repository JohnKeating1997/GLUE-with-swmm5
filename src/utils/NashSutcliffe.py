# calculate the Nash-Sutcliffe efficiency coefficient
import os
import numpy as np
import pandas as pd

# config the path
config = {
  'publicPath': os.path.abspath(os.path.join(os.getcwd())),
  'observed_data': 'result.csv',
  'simulated_data': 'result.csv',
}
config['observed_data_path'] = os.path.join(config['publicPath'],'mock','observed',config['observed_data'])
config['simulated_data_path'] = os.path.join(config['publicPath'],'mock','random',config['simulated_data'])

def calculateNashSutcliffe(observed_data_path = config['observed_data_path'], simulated_data_path = config['simulated_data_path']):
  # read the csvs
  df_observed = pd.read_csv(observed_data_path, index_col=False)
  df_simulated = pd.read_csv(simulated_data_path, index_col=False)
  # get all the indexes without duplicates
  indexes = list(set((df_observed['INDEX'])))
  # calculate the Nash-Sutcliffe efficiency coefficient
  NS_list = []
  for index in indexes:
    curObservedDf = df_observed.loc[df_observed['INDEX'] == indexes[0]]
    curSimulatedDf = df_simulated.loc[df_simulated['INDEX'] == indexes[0]]
    if len(curObservedDf) != len(curSimulatedDf):
      raise Exception('data observed and simulated don\'t match')
    length = len(curSimulatedDf)
    observedAveg = 0
    # calculate the average observed data
    for i in range(length):
      observedAveg += df_observed['VALUE'].iloc[i]
    observedAveg /= length
    # calculate the rest of Nash-Sutcliffe efficiency coefficient
    numerator = 0
    denominator = 0
    for i in range(length):
      numerator += np.square(df_observed['VALUE'].iloc[i] - df_simulated['VALUE'].iloc[i])
      denominator += np.square(df_observed['VALUE'].iloc[i] - observedAveg)
    NS_list.append(1 - numerator / denominator)
  # calculate the average of the NS_list
  NS = sum(NS_list) / len(NS_list)
  return NS

if __name__ == '__main__':
  print(calculateNashSutcliffe())
