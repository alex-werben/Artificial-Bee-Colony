from __future__ import annotations
import numpy as np
from copy import deepcopy
import os


class FoodSource:
    def __init__(self,
                 lower_limit: float = -5.0,
                 upper_limit: float = 5.0,
                 nectar: float = 1000.0,
                 probability: float = 0.0,
                 dimensions: int = 2
                 ) -> None:
        self._lower_limit = lower_limit
        self._upper_limit = upper_limit
        self._nectar = nectar
        self._probability = probability
        self._dimensions = dimensions
        self._trial_count = 0
        self._fn_val = 0
        self._id = ""
        self._parameters = []

    def __lt__(self, other: FoodSource) -> bool:
        return self.get_nectar() < other.get_nectar()

    def evaluate_nectar(self) -> float:
        self.set_fn_val(self.function_value())

        nectar = 0.0

        # nectar = self.get_fn_val()
        #
        # return nectar

        if self.get_fn_val() >= 0:
            nectar = 1.0 / (1.0 + self.get_fn_val())
        else:
            nectar = 1.0 + abs(self.get_fn_val())

        return nectar

    def get_id(self) -> str:
        return self._id

    def get_fn_val(self) -> float:
        return self._fn_val

    def reset_trial_count(self) -> None:
        self._trial_count = 0

    def increment_trial_count(self) -> None:
        self._trial_count += 1

    def get_trial_count(self) -> int:
        return self._trial_count

    def get_parameters(self) -> list:
        return self._parameters

    def get_probability(self) -> float:
        return self._probability

    def get_nectar(self) -> float:
        return self._nectar

    def get_neighboring(self, neighbor_food_source: FoodSource) -> FoodSource:
        """
        Get new FoodSource from an old one with some random modification.
        :return: FoodSource
        """
        dim = np.random.randint(self._dimensions)
        phi = np.random.uniform(-1, 1)

        params = deepcopy(self._parameters)

        new_param = self._parameters[dim] + \
            phi * (self._parameters[dim] - neighbor_food_source.get_parameters()[dim])

        params[dim] = new_param

        new_food_source = deepcopy(self)
        new_food_source.set_parameters(params)

        return new_food_source

    def set_parameters(self, parameters: list = None) -> None:
        if not parameters:
            for i in range(self._dimensions):
                param = np.random.uniform(self._lower_limit, self._upper_limit)
                self._parameters.append(param)
        else:
            self._parameters = parameters
        self._nectar = self.evaluate_nectar()
        self._id = self.generate_id()

    def generate_id(self) -> str:
        identifier = ""
        for param in self.get_parameters():
            identifier += str(param)
        return identifier
        # return np.random.randint(1, 10e6)

    def set_probability(self, probability: float) -> None:
        self._probability = probability

    def set_fn_val(self, fn_val: float) -> None:
        self._fn_val = fn_val

    def function_value(self) -> float:
        """
        Calculate optimization function with specific parameters.
        """
        fn_val = 0.0

        x1, x2 = self.get_parameters()

        fn_val = (x1**2 + x2 - 11)**2 + (x1 + x2**2 - 7)**2

        # for x in self.get_parameters():
        #     fn_val += x ** 2

        return fn_val

    def log_data(self, cycle: int, index: int) -> None:
        line = f"{cycle},"
        for p in self.get_parameters():
            line += f"{p},"
        line += "\n"
        os.makedirs(f"data/train/", exist_ok=True)

        with open(f"data/train/{index}.csv", 'a') as fp:
            fp.write(line)

    def log_best(self, cycle: int, index: int) -> None:
        os.makedirs("data/best/", exist_ok=True)
        line = f"{cycle},"
        for p in self.get_parameters():
            line += f"{p},"
        line += '\n'
        with open(f"data/best/{index}.csv", 'a') as fp:
            fp.write(line)