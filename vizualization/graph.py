import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd


def make_data():
    x = np.arange(-5, 5, 0.05)
    y = np.arange(-5, 5, 0.05)
    xgrid, ygrid = np.meshgrid(x, y)

    # z = xgrid**2 + ygrid**2
    z = (xgrid ** 2 + ygrid - 11) ** 2 + (xgrid + ygrid ** 2 - 7) ** 2
    return xgrid, ygrid, z


fig, ax = plt.subplots()


def plot_food_sources(i):
    for index in range(fs_num):
        x1_next, x2_next = df[index][1][i], df[index][2][i]
        ax.scatter(x1_next, x2_next, c='b')
        if i > 0:
            x1_prev, x2_prev = df[index][1][i - 1], df[index][2][i - 1]
            plt.plot((x1_prev, x1_next), (x2_prev, x2_next), c='b')


def plot_best_solutions(i):
    for index in range(num_solutions):
        x1_next, x2_next = best_solutions[index][1][i], best_solutions[index][2][i]
        ax.scatter(x1_next, x2_next, c='r')
        if i > 0:
            x1_prev, x2_prev = best_solutions[index][1][i - 1], best_solutions[index][2][i - 1]
            plt.plot((x1_prev, x1_next), (x2_prev, x2_next), c='r')

def animate(i):
    ax.clear()
    ax.contour(x, y, z, levels=50)

    plot_food_sources(i)
    plot_best_solutions(i)

    ax.text(0, 1.05, f"{i}", ha="center", va="center", transform=ax.transAxes, bbox=dict(facecolor="none"))


def main():
    ani = animation.FuncAnimation(fig, animate, params['max_cycles'] - 1,
                                  interval=400, blit=False)

    plt.show()


if __name__ == '__main__':
    params = {}
    with open("../config.cfg") as fp:
        lines = fp.readlines()
        for line in lines:
            key, val = line.split(":")
            params[key] = int(val)

    fs_num = params["colony_size"] // 2
    num_solutions = params["num_solutions"]

    df = [pd.read_csv(f"../data/train/{index}.csv",
                      header=None,
                      index_col=0,
                      usecols=[0, 1, 2]
                      ) for index in range(fs_num)]
    best_solutions = [pd.read_csv(f"../data/best/{index}.csv",
                                  header=None,
                                  index_col=0,
                                  usecols=[0, 1, 2]
                                  ) for index in range(num_solutions)]

    x, y, z = make_data()
    main()
