import os
import shutil
import numpy as np
from multiprocessing import Process, Lock, Pool

from src.artificial_bee_colony import ArtificialBeeColony


def experiment1():
    X = [2, 4, 8, 16, 32, 64]
    lambda_ = 0.01
    a = 10
    iterations = []
    for size in X:
        eps_ = lambda_ * a * np.sqrt(size)
        solution_ = np.array([0] * size)
        abc = ArtificialBeeColony(
            solution=solution_,
            eps=eps_,
            colony_size=20,
            num_solutions=1,
            dimensions=size
        )
        iteration_num = abc.experiment1()
        iterations.append(iteration_num)
        print(f"|X|={size}, iteration_num={iteration_num}")
    print(iterations)

def experiment2():
    X = [2, 4, 8, 16, 32, 64]
    lambda_ = 0.01
    a = 10
    starts = 20
    iterations = []
    exp_f_arr = []
    exp_x_arr =[]
    for index, size in enumerate(X):
        iterations.append([])
        exp_f_arr.append([])
        exp_x_arr.append([])
        eps_ = lambda_ * a * np.sqrt(size)
        solution_ = np.array([0] * size)
        for start in range(starts):
            abc = ArtificialBeeColony(
                solution=solution_,
                eps=eps_,
                colony_size=20,
                num_solutions=1,
                dimensions=size
            )
            iteration_num, exp_f, exp_x = abc.experiment3()
            iterations[index].append(iteration_num)
            exp_f_arr[index].append(exp_f)
            exp_x_arr[index].append(exp_x)
            print(f"|X|={size}, start={start}")
        with open("jupyter/data1.csv", "a") as fp:
            fp.write(f"{size},{np.mean(iterations[index])},{np.mean(exp_f_arr[index])},{np.mean(exp_x_arr[index])}\n")

        print(f"iterations_num={np.mean(iterations[index])},"
              f"exp_f={np.mean(exp_f_arr[index])},"
              f"exp_x={np.mean(exp_x_arr[index])}")

def experiment3():
    X = [2, 4, 8, 16, 32, 64]
    lambda_ = 0.01
    a = 10
    starts = 20
    success_prob_arr = []
    exp_f_arr = []
    exp_x_arr = []
    for index, size in enumerate(X):
        success_prob_arr.append([])
        exp_f_arr.append([])
        exp_x_arr.append([])
        eps_ = lambda_ * a * np.sqrt(size)
        solution_ = np.array([0] * size)
        for start in range(starts):
            abc = ArtificialBeeColony(
                solution=solution_,
                eps=eps_,
                colony_size=20,
                num_solutions=1,
                dimensions=size
            )
            success_prob, exp_f, exp_x = abc.experiment3()
            success_prob_arr[index].append(success_prob)
            exp_f_arr[index].append(exp_f)
            exp_x_arr[index].append(exp_x)
            print(f"|X|={size}, start={start}")
        with open("jupyter/exp3.csv", "a") as fp:
            fp.write(f"{size},{np.mean(success_prob_arr[index])},{np.mean(exp_f_arr[index])},{np.mean(exp_x_arr[index])}\n")

        print(f"success_prob={np.mean(success_prob_arr[index])},"
              f"exp_f={np.mean(exp_f_arr[index])},"
              f"exp_x={np.mean(exp_x_arr[index])}")

def exp(iterations, lock, size: int, i: int):
    solution = np.array([0] * size)
    lambda_ = 0.1
    a = 10
    eps = lambda_ * a * np.sqrt(size)
    abc = ArtificialBeeColony(
        solution=solution,
        eps=eps,
        colony_size=40,
        num_solutions=1,
        dimensions=size
    )
    iteration_num = abc.experiment1()
    print(f"|X|={size}, iteration_num={iteration_num}")
    lock.acquire()
    iterations[0].append(iteration_num)
    # print(iterations)
    lock.release()
    return iteration_num



def experiment_iterations():
    """
    Find required number of iterations to get desired accuracy.
    Multistart = 100
    X = [2, 4, 8, 16, 32, 64]
    """
    X = [2, 4, 8, 16, 32, 64]
    multistart = 100
    lock = Lock()
    iterations = []
    procs = []
    for index, size in enumerate(X):
        iterations.append([])
        pool = Pool(processes=4)
        r = pool.map(exp, (iterations[index], lock, size, 0))
        # for i in range(4):
        #     proc = Process(target=exp, args=(iterations, lock, size, i))
        #     procs.append(proc)
        #     proc.start()

        # for p in procs:
        #     p.join()


        print(r)
        break

        with open("jupyter/data1.csv", "a") as fp:
            fp.write(f"{size},{np.mean(iterations[index])}\n")


def main():
    shutil.rmtree("data/")
    os.mkdir("data/")

    params = {}
    with open("config.cfg") as fp:
        lines = fp.readlines()
        for line in lines:
            key, val = line.split(":")
            params[key] = int(val)

    experiment_iterations()

    # experiment3()




if __name__ == "__main__":
    main()
