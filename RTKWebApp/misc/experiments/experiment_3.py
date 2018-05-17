import apogee as ap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

f = pd.DataFrame.from_csv("./data/apt15074_sensor.csv")
arr = np.array(f[["temp", "rh"]])

k = ap.KalmanFilter(n=2, m=2, qs=1.0, rs=50.0)
kd = k.filter(arr, mode=1)
ld = k.likelihood(arr)
dt, dh = arr[:, 0], arr[:, 1]
kt, kh = kd[:, 0], kd[:, 1]

print ap.rmse(kt, dt)
plt.subplot(3, 1, 1)
plt.plot(dt[100:500])
plt.plot(kt[100:500])
plt.subplot(3, 1, 2)
plt.plot(ld[:, 0])
plt.subplot(3, 1, 3)
plt.plot((kt[100:500]-dt[100:500])**2.0)
plt.show()