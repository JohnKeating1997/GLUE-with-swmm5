# calculate the statistical property of a parameter based on likelyhood
import numpy as np
def calculateMuAndSigma(candidates,rambda):
  '''
  description: calculated the likehood average and variance
  :param :: candidates <[[value1, likelyhood1], [value2, likelyhood2], [value3, likelyhood3], ...]>
  :param :: rambda <float> the the threshold of acceptance
  return :: statistics {mu: float, sigma: float}
  '''
  sum_likelyhood = 0
  mu = 0
  sigma = 0
  for i,v in enumerate(candidates):
    if v > rambda:
      sum_likelyhood += v[1]
  for i,v in enumerate(candidates):
    if v > rambda:
      mu += v[1] / sum_likelyhood * v[0]
  for i,v in enumerate(candidates):
    if v > rambda:
      sigma += v[1] / sum_likelyhood * np.square(v[0] - mu)
  return {'mu': mu, 'sigma': sigma}