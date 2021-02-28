# monte-carlo methods
import numpy as np
import random
# temporarily set the identical startTime & endTime for every pipes
def splitRDIIRandomlyIntoPipes(RDII, pipes, startTime, endTime):
  '''
  description: split the RDII randomly into different pipes
  :param RDII(LPS)
  :param pipes:: all the pipes that need to init rdii flows. [pipe1s <string>, pipe2 <string>,...]
  :param startTime:: [startTime1 <string>, startTime2 <string>, ...] the start time of the rdii
  :param endTime:: [endTime1 <string>, endTime2 <string>] the end time of the rdii
  :return:: scenario: [[pipe1 <string>, inflow1 <float>, startTime1: <string>, endTime1: <string>],
                     [pipe2 <string>,inflow2 <float>, startTime2: <string>, endTime2: <string>],...]
  '''
  split = [0] # 0 is the start
  for i in range(len(pipes) - 1):
    # no need to set the random seed in python
    split.append(random.random())
  # sort the split numbers
  split.sort() # ascendent sort
  split.append(1) # 1 is the end

  scenario = []
  idx = 1
  while(idx < len(split)):
    curRDII = RDII * (split[idx] - split[idx - 1])
    scenario.append([pipes[idx - 1], curRDII, startTime[idx - 1], endTime[idx - 1]])
    idx += 1
  
  return scenario

# print(splitRDIIRandomlyIntoPipes(100,[1,2,3,4,5],1,1))
