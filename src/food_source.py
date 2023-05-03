from __future__ import annotations
import numpy as np
from copy import deepcopy


class FoodSource:
    def __init__(self,
                 lower_limit_: float = -1,
                 upper_limit_: float = 1,
                 nectar: float = 1000,
                 probability: float = 0,
                 dimensions_: int = 2
                 ) -> None:
        self.lower_limit = lower_limit_
        self.upper_limit = upper_limit_
        self._nectar = nectar
        self._probability = probability
        self.dimensions = dimensions_
        self._trial_count = 0
        self._fn_val = 0
        self._id = np.random.randint(1, 10e6)
        self._parameters = []
        for i in range(self.dimensions):
            param = np.random.uniform(self.lower_limit, self.upper_limit)
            self._parameters.append(param)

    def __lt__(self, other: FoodSource) -> bool:
        return self.get_nectar() < other.get_nectar()

    def evaluate_nectar(self) -> float:
        self.set_fn_val(self.function_value())

        nectar = 0.0

        if self.get_fn_val() > 0:
            nectar = 1.0 / (1.0 + self.get_fn_val())
        else:
            nectar = 1 + abs(self.get_fn_val())

        return nectar

    def get_id(self) -> int:
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
        dim = np.random.randint(self.dimensions)

        phi = np.random.uniform(-1, 1)

        params = deepcopy(self._parameters)

        new_param = self._parameters[dim] + \
            phi * (self._parameters[dim] - neighbor_food_source.get_parameters()[dim])

        params[dim] = new_param

        new_food_source = deepcopy(self)
        new_food_source.set_parameters(params)

        return new_food_source

    def set_parameters(self, parameters_: list) -> None:
        self._nectar = self.evaluate_nectar()
        self._parameters = parameters_

    def set_probability(self, probability: float) -> None:
        self._probability = probability

    def set_fn_val(self, fn_val: float) -> None:
        self._fn_val = fn_val

    def function_value(self) -> float:
        fn_val = 0.0

        for x in self.get_parameters():
            fn_val += x ** 2

        return fn_val
