import os
import shutil

from src.artificial_bee_colony import ArtificialBeeColony


def main():
    shutil.rmtree("data/")
    os.mkdir("data/")

    params = {}
    with open("config.cfg") as fp:
        lines = fp.readlines()
        for line in lines:
            key, val = line.split(":")
            params[key] = int(val)

    abc = ArtificialBeeColony(
        max_cycles=params["max_cycles"],
        colony_size=params["colony_size"],
        num_solutions=params["num_solutions"],
    )
    abc.run()


if __name__ == "__main__":
    main()
