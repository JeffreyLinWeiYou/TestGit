# coding=UTF-8
'''
Created on 2015年11月4日

@author: ben
'''
import numpy as np
import matplotlib.pyplot as plt

if __name__ == '__main__':
    N = 10000
    x = 3*(np.random.rand(N)-0.5)
    print x
    y = 3*(np.random.rand(N)-0.5)
#      colors = np.random.rand(N)
#     area = np.pi * (15 * np.random.rand(N))**2  # 0 to 15 point radiuses
 
    plt.scatter(x, y, alpha=0.5)
    plt.show()

#     fig = plt.figure()
#     ax = fig.add_subplot(111)
#     t = ax.scatter(np.random.rand(20), np.random.rand(20))
#     ax.collections
#     fig.show()

    pass