import talib
from pprint import pprint
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(0)
close = np.random.random(250)
sma = talib.SMA(close, timeperiod=10)
plt.figure(figsize=(11,3))
plt.plot(close, "r-")
plt.plot(sma, "b-")
plt.show()





