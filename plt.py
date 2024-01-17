import matplotlib.pyplot as plt
import numpy as np

X = [100, 200, 300, 400, 500, 600, 700, 800, 900, 1000]
Y1 = np.array([0.03, 0.06, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08, 0.08])
Y2 = np.array([0.006, 0.012, 0.018, 0.022, 0.028, 0.036, 0.041, 0.048, 0.051, 0.055])
Y3 = np.array([0.011, 0.012, 0.013, 0.015, 0.017, 0.020, 0.021, 0.022, 0.025, 0.027])
Y4 = np.array([0.0016, 0.0032, 0.0047, 0.0064, 0.0079, 0.0095, 0.0111, 0.01252, 0.01401, 0.01572])
Y5 = np.array([0.0037, 0.0075, 0.0113, 0.0150, 0.0188, 0.0227, 0.0265, 0.0303, 0.0337, 0.0376])


# 绘图
plt.xlabel("NUmber of matching entries")
plt.ylabel("Search time(s)")
plt.xlim((100, 1000))
plt.ylim((0.01, 0.04))
my_x_ticks = np.arange(100, 1100, 100)
my_y_ticks = np.arange(0, 0.045, 0.01)
plt.xticks(my_x_ticks)
plt.yticks(my_y_ticks)
plt.plot(X, Y1, marker="v", color='g', label='Sophos')
plt.plot(X, Y2, marker="^", color='b', label='Mitra')
plt.plot(X, Y3, marker="s", color='c', label='CLOSE-FB')
plt.plot(X, Y4, marker=".", color='b', label='most_simple_ELS')
plt.plot(X, Y5, marker=".", color='r', label='most_complex_ELS')

plt.grid(axis='y')
plt.legend()

plt.show()

# plt.savefig()