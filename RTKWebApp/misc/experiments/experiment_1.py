import apogee as ap
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

f = pd.DataFrame.from_csv("./data/apt15074_sensor.csv")
arr = np.array(f[["temp", "rh"]])

k = ap.KalmanFilter(qs=5.0, n=2, m=2)
# k.Q = np.identity(2)
k.Q = np.cov(arr.T)
print k.Q.shape
d = np.zeros((100, 100))
c = 1

for i in range(len(arr)):
    k.filter_step(arr[i])

    if i % 1000 == 0:
        m = ap.MVNormal(k.x.squeeze(), k.P, labels=["Temperature", "Humidity"])
        xr, yr = np.linspace(0, 100, 100), np.linspace(0, 100, 100)
        d += m.mesh((xr, yr))

        c += 1
    print i


plt.contour(d/float(c),linewidths=0.5,colors='k')
plt.imshow(d/float(c), cmap=plt.cm.jet, aspect="auto")
plt.colorbar()
plt.scatter(arr[:, 0], arr[:, 1], marker="x", s=5, c="k")
plt.title("Graph Showing Average Probability Density over 10000 Sensor Readings")
plt.xlabel("Temperature (F)")
plt.ylabel("Relative Humidity (%)")
plt.xlim(60, 80)
plt.ylim(10, 80)
plt.legend()
plt.show()
