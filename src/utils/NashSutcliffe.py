# calculate the Nash-Sutcliffe efficiency coefficient
import os
import numpy as np

# config the path
config = {
  'publicPath': os.path.abspath(os.path.join(os.getcwd())),
  'observed_data': 'observed_date.csv',
  'simulated_data': 'simulated_data.csv',
}
config['observed_data_path'] = os.path.join(config['publicPath'],'mock','observed',config['observed_data'])
config['simulated_data_path'] = os.path.join(config['publicPath'],'mock','random',config['simulated_data'])

