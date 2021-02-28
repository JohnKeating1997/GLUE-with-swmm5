import sys
import os
from sys import path
from swmm5.swmm5tools import SWMM5Simulation

# config environment
config = {
  'publicPath': os.path.abspath(os.path.join(os.getcwd()))
}
config['utils'] = os.path.join(config['publicPath'], 'src', 'utils')
# add the public path to the sys.path
path.append(config['publicPath'])

from src.utils.MonteCarlo import splitRDIIRandomlyIntoPipes
from src.utils.modifyInp import setFlowOnAverage
from src.utils.runSwmm5 import runSimulation
from src.utils.NashSutcliffe import calculateNashSutcliffe
from src.utils.statistics import calculateMuAndSigma

# set the iteration times
ITERATION_TIMES = 5
# total RDII of the sewer systems
RDII = 84 # LPS
if __name__ == "__main__":
  # 0. set a mock example-case.inp (DONE)
  # setFlowOnAverage([['37', 48, '03:00','10:30'],['53', 36, '03:00','10:30']], 
  #                 out_file_path = os.path.join(config['publicPath'], 'mock', 'observed', 'example-case.inp'))
  # 1. get the try-case result (DONE)
  # exampleCaseInpPath = os.path.join(config['publicPath'], 'mock', 'observed', 'example-case.inp')
  # exampleCaseOutPath = os.path.join(config['publicPath'], 'mock', 'observed', 'result.csv')
  # runSimulation(['NODE'] * 4, ['13', '36', '57', '64'], [0, 0, 0, 4], exampleCaseInpPath, exampleCaseOutPath)

  # 2. start GLUE
  inpFilePath = os.path.join(config['publicPath'], 'mock', 'random', 'try-case.inp')
  outFilePath = os.path.join(config['publicPath'], 'mock', 'random', 'result.csv')
  st = SWMM5Simulation(os.path.join(config['publicPath'], 'static', 'baseline.inp'))
  links = st.Link()

  cnt = 0
  startTime = ['03:00'] * len(links)
  endTime = ['10:30'] * len(links)

  # log Nash-Sutcliffe efficiency coefficient of every iteration
  NS_log = []
  # log scenario coefficient of every iteration
  scenario_log = []
  while cnt < ITERATION_TIMES:
    # 2.1 parameter sampling (prior distribution: uniform distribution)
    scenario = splitRDIIRandomlyIntoPipes(RDII = RDII, pipes = links, startTime = startTime, endTime = endTime)
    scenario_log.append(scenario)
    setFlowOnAverage(scenario)
    # 2.2 run the simulation
    runSimulation(['NODE'] * 4, ['13', '36', '57', '64'], [0, 0, 0, 4], inpFilePath, outFilePath)
    # 2.3 calculate the Nash-Sutcliffe efficiency coefficient as the likelyhood
    NS = calculateNashSutcliffe()
    NS_log.append(NS)
    # 
    cnt += 1
    print('ITERATION:', cnt)
  # 2.4 after the iteration, generate the candidates
  pipesCandidates = {}
  for i,v in enumerate(links):
    pipesCandidates[v] = []
  for i in range(ITERATION_TIMES):
    for j,v in enumerate(links):
      pipesCandidates[v].append([scenario_log[i][j][1], NS_log[i]])
  # 2.5 calculate the statistical property of every scenario
  pipeStatistics = {}
  for pipe in pipesCandidates:
    pipeStatistics[pipe] = calculateMuAndSigma(pipesCandidates[pipe], rambda = 0.6)
  # 2.6 print the result
  print(pipeStatistics)

