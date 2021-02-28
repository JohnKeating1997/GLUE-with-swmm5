import sys
import os
from sys import path

# config environment
config = {
  'publicPath': os.path.abspath(os.path.join(os.getcwd()))
}
config['utils'] = os.path.join(config['publicPath'], 'src', 'utils')
# add the public path to the sys.path
path.append(config['publicPath'])

from src.utils.runSwmm5 import runSimulation
from src.utils.modifyInp import setFlowOnAverage
if __name__ == "__main__":
  # 0. set a mock example-case.inp (DONE)
  # setFlowOnAverage([['37', 48],['53', 36]],'03:00','10:30', out_file_path = os.path.join(config['publicPath'], 'mock', 'observed', 'example-case.inp'))

  # 1. get the try-case result (DONE)
  # exampleCaseInpPath = os.path.join(config['publicPath'], 'mock', 'observed', 'example-case.inp')
  # exampleCaseOutPath = os.path.join(config['publicPath'], 'mock', 'observed', 'result.csv')
  # runSimulation(['NODE'] * 4, ['13', '36', '57', '64'], [0, 0, 0, 4], exampleCaseInpPath, exampleCaseOutPath)