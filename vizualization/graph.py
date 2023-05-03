import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd
import os

def make_data():
    x = np.arange(-1, 1, 0.05)
    y = np.arange(-1, 1, 0.05)
    xgrid, ygrid = np.meshgrid(x, y)

    z = xgrid**2 + ygrid**2
    return xgrid, ygrid, z

fig, ax = plt.subplots()

def animate(i):
    ax.clear()
    # print(i)
    ax.contour(x, y, z, levels=20)
    # cs.clabel(colors='black', inline=False)
    with open("../data/best/best.csv") as fp:
        lines = fp.readlines()
        arr = lines[i].split(",")
        x1, x2 = float(arr[1]), float(arr[2])
        ax.scatter(x1, x2)
        if i > 0:
            arr0 = lines[i-1].split(",")
            x10, x20 = float(arr0[1]), float(arr0[2])
            plt.plot((x10, x1), (x20, x2))

    ax.text(0, 1.05, f"{i}", ha="center", va="center", transform=ax.transAxes, bbox=dict(facecolor="none"))


if __name__ == '__main__':
    x, y, z = make_data()

    ani = animation.FuncAnimation(fig, animate, 99, interval=200, blit=False)

    plt.show()