import numpy as np
from copy import deepcopy


class FoodSource:
    def __init__(self,
                 lower_limit_=-1,
                 upper_limit_=1,
                 nectar_=1000,
                 probability_=0,
                 dimensions_=2):
        self.lower_limit = lower_limit_
        self.upper_limit = upper_limit_
        self._nectar = nectar_
        self._probability = probability_
        self.dimensions = dimensions_
        self._trial_count = 0
        self._id = np.random.randint(1, 10e6)
        self.parameters = []

    def __lt__(self, other):
        return self.get_nectar() < other.get_nectar()

    def initialize(self):
        for i in range(self.dimensions):
            param = np.random.uniform(self.lower_limit, self.upper_limit)
            self.parameters.append(param)

    def get_id(self):
        return self._id

    def reset_trial_count(self) -> None:
        self._trial_count = 0

    def increment_trial_count(self) -> None:
        self._trial_count += 1

    def get_trial_count(self) -> int:
        return self._trial_count

    def set_parameters(self, parameters_: list) -> None:
        self.parameters = parameters_

    def get_probability(self):
        return self._probability

    def get_nectar(self):
        return self._nectar

    def get_neighboring(self, neighbor_food_source):
        """
        Get new FoodSource from an old one with some random modification.
        :return: FoodSource
        """
        dim = np.random.randint(self.dimensions)

        phi = np.random.uniform(-1, 1)

        params = deepcopy(self.parameters)

        new_param = self.parameters[dim] + \
            phi * (self.parameters[dim] - neighbor_food_source.parameters[dim])

        params[dim] = new_param

        new_food_source = deepcopy(self)
        new_food_source.set_parameters(params)

        return new_food_source
