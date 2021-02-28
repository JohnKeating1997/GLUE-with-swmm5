import math
import numpy as np
import matplotlib.pyplot as plt
import os

def plotNormalDistribution(mu, sigma, outputPath):
  '''
  description: plot the normal distribution and save the image
  :param :: mu
  :param :: sigma
  return :: void
            generate the images
  '''
  # reset the canvas
  # plt.cla()
  # x = np.linspace(mu - 3 * sigma, mu + 3 * sigma, 50)   # 定义域
  x = np.linspace(-5, 10, 200)
  y = np.exp(-(x - mu) ** 2 / (2 * sigma ** 2)) / (math.sqrt(2 * math.pi) * sigma) # 定义曲线函数
  plt.plot(x, y, "g", linewidth = 2)    # 加载曲线
  plt.grid(True)  # 网格线

  # save the images
  path = os.path.split(outputPath)[0]
  if not os.path.exists(path):
    os.makedirs(path)
  plt.savefig(outputPath)
  