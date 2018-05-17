import apogee as ap
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import multivariate_normal

f = pd.DataFrame.from_csv("./data/apt15074_sensor.csv")
arr = np.array(f[["temp", "rh"]])

x = np.array([np.linspace(40, 90, 100), np.linspace(10, 95, 100)]).reshape(2, 100)
cov = np.cov(arr.T)
mean = np.mean(arr.T, axis=1)
print mean, cov

m1 = ap.Normal(mean, cov, labels=["A", "B"]).pdf(x.T)
# m2 = multivariate_normal(mean=mean, cov=cov).pdf(np.meshgrid(np.linspace(40, 90, 100), np.linspace(10, 95, 100)))
# print np.sum(m1 - m2)  # show equivalence (should be correct to less than 1e-16)

m = ap.Normal(mean, cov, labels=["A", "B"]).mesh((np.linspace(0, 100, 100), np.linspace(0, 100, 100)))

plt.contour(m,linewidths=0.5,colors='k')
plt.imshow(m, cmap=plt.cm.jet, aspect="auto")
plt.colorbar()
plt.scatter(arr[:, 0], arr[:, 1], marker="x", s=5, c="k")
plt.title("Graph Showing Probability Density Distribution for 10000 Sensor Readings")
plt.xlabel("Temperature (F)")
plt.ylabel("Relative Humidity (%)")
plt.xlim(60, 80)
plt.ylim(10, 80)
plt.legend()
plt.show()
