# monte-carlo methods
import numpy as np

def splitRDIIRandomlyIntoPipes(RDII,pipes):
  '''
  description: split the RDII randomly into different pipes
  :param structure: <[string] | string> type of structure,such as 'SUBCATCH', 'NODE', 'LINK', 'SYS'
  :param index: <[string] | string> index of specified structure of which the result will be written into xxx.csv
  :param inp_file_path: <string> absolute path of inp file
  :param out_file_path: <string> absolute path of output file
  
  :return: void
    generate a csv file to save the result
  '''