from __future__ import annotations
from src.food_source import FoodSource
import numpy as np


class ArtificialBeeColony:
    def __init__(self,
                 solution: np.array = None,
                 eps: float = 0.1,
                 max_cycles: int = 10,
                 colony_size: int = 5,
                 num_solutions: int = 1,
                 dimensions: int = 2,
                 ) -> None:
        self.best_food_sources = None
        self._max_cycles = max_cycles
        self._colony_size = colony_size
        self._max_food_sources = colony_size // 2
        self.food_sources: list[FoodSource] = []
        self._trial_limit = colony_size
        self._num_solutions = num_solutions
        self._solution = solution
        self._eps = eps
        self._dimensions = dimensions

    def get_trial_limit(self) -> int:
        return self._trial_limit

    def get_new_based_on(self, food_source: FoodSource, fs_num: int) -> FoodSource:
        """
        Get new food source based on an old one and its neighbor.
        """
        fs_count = self._max_food_sources
        neighbor_fs_num = np.random.randint(0, fs_count - 1)

        # to eliminate picking itself
        if neighbor_fs_num == fs_num:
            neighbor_fs_num += 1

        new_food_source = food_source.get_neighboring(self.food_sources[neighbor_fs_num])

        return new_food_source

    def get_nearest_neighbor(self, food_source: FoodSource, fs_num: int) -> FoodSource:
        """
        Get new food source based on modified nearest neighbor.
        """
        s: list[FoodSource] = []
        dist = 10e2
        nearest_neighbor = None

        # Create set of better solutions
        for i in range(self._max_food_sources):
            if i == fs_num:
                continue
            if self.food_sources[i].get_nectar() > food_source.get_nectar():
                s.append(self.food_sources[i])

        # Find nearest neighbor
        if len(s) > 0:
            for fs in s:
                current_dist = np.linalg.norm(np.array(fs.get_parameters()) - np.array(food_source.get_parameters()))
                if current_dist < dist:
                    nearest_neighbor = fs
                    dist = current_dist
        else:
            return food_source

        new_food_source = food_source.get_neighboring(nearest_neighbor)

        return new_food_source

    def generate_new_food_source(self) -> FoodSource:
        new_food_source = FoodSource(dimensions=self._dimensions)
        new_food_source.set_parameters()
        return new_food_source

    def initialize_food_sources(self) -> None:
        """
        Setup random food sources.
        """
        for _ in range(self._max_food_sources):
            self.food_sources.append(self.generate_new_food_source())

    def send_employed_bees(self) -> None:
        """
        Send in employed bees for food.
        Employed bees return with nectar.
        """
        for fs_num in range(len(self.food_sources)):
            new_food_source = self.get_new_based_on(self.food_sources[fs_num], fs_num)
            # new_food_source = self.get_nearest_neighbor(self.food_sources[fs_num], fs_num)

            if self.food_sources[fs_num].get_nectar() < new_food_source.get_nectar():
            # if self.food_sources[fs_num].get_nectar() > new_food_source.get_nectar():
                self.food_sources[fs_num] = new_food_source
            else:
                self.food_sources[fs_num].increment_trial_count()

    def update_probabilities(self) -> None:
        """
        Update desirability of food sources.
        Onlooker bees will now pick food source and
        explore the neighborhood, replacing with better
        food sources when found.
        """
        # nectar_sum = reduce(lambda acc, food_source: acc + food_source.get_nectar(), self.food_sources)
        nectar_sum = 0
        for fs in self.food_sources:
            nectar_sum += fs.get_nectar()

        for fs in self.food_sources:
            fs.set_probability(fs.get_nectar() / nectar_sum)

    def send_onlooker_bees(self) -> None:
        """
        Onlooker bee perceives the amount of nectar
        that each employed bee got from its food
        source with some error.
        Onlooker bee picks food source, from which
        more nectar was brought.
        """
        onlookers = self._max_food_sources

        for onlooker in range(onlookers):
            r = np.random.uniform(0, 1)
            prop_sum = 0

            for fs_num, food_source in enumerate(self.food_sources):
                prop_sum += food_source.get_probability()

                if r <= prop_sum:
                    new_food_source = self.get_new_based_on(food_source, fs_num)
                    # new_food_source = self.get_nearest_neighbor(food_source, fs_num)

                    if food_source.get_nectar() < new_food_source.get_nectar():
                    # if food_source.get_nectar() > new_food_source.get_nectar():
                        self.food_sources[fs_num] = new_food_source
                    else:
                        food_source.increment_trial_count()
                    break

    def memorize_best_food_sources(self) -> None:
        """
        Memorize the best food source for this cycle.
        """
        food_sources_map = {}
        for food_source in self.food_sources:
            if not food_sources_map.get(food_source.get_id()):
                food_sources_map[food_source.get_id()] = food_source
            else:
                if food_sources_map[food_source.get_id()].get_nectar() < food_source.get_nectar():
                # if food_sources_map[food_source.get_id()].get_nectar() > food_source.get_nectar():
                    food_sources_map[food_source.get_id()] = food_source

        unique_food_sources = list(food_sources_map.values())
        unique_food_sources.sort()

        self.best_food_sources = unique_food_sources[:self._num_solutions]
        for fs in self.best_food_sources:
            fs.reset_trial_count()

    def send_scout_bees(self) -> None:
        """
        Scouts find random new food sources which
        may be either better or worse than the old one.
        """
        trial_limit = self.get_trial_limit()

        # for fs_num, food_source in enumerate(self.food_sources):
        #     if food_source.get_trial_count() >= trial_limit:
        #         new_food_source = self.generate_new_food_source()
        #         self.food_sources[fs_num] = new_food_source

        max_trial_fs = self.food_sources[0]
        max_trial_fs_num = 0
        for fs_num, food_source in enumerate(self.food_sources):
            if food_source.get_trial_count() > max_trial_fs.get_trial_count():
                max_trial_fs = food_source
                max_trial_fs_num = fs_num

        if max_trial_fs.get_trial_count() > trial_limit:
            new_food_source = self.generate_new_food_source()
            self.food_sources[max_trial_fs_num] = new_food_source

    def experiment1(self) -> int:
        """
        Find number of required iterations to get desired accuracy of solution.
        """
        best_food_source = None

        self.initialize_food_sources()
        self.memorize_best_food_sources()
        cycle = 0
        while abs(np.linalg.norm(np.array(self.best_food_sources[0].get_parameters()) - self._solution)) > self._eps:
            if cycle % 1000 == 0:
                print(f"Cycle: {cycle}")
            self.send_employed_bees()

            self.update_probabilities()

            self.send_onlooker_bees()

            self.memorize_best_food_sources()

            self.send_scout_bees()
            cycle += 1

        return cycle

    def experiment2(self):
        best_food_source = None

        self.initialize_food_sources()
        self.memorize_best_food_sources()
        cycle = 0
        while abs(np.linalg.norm(np.array(self.best_food_sources[0].get_parameters()) - self._solution)) > self._eps:
            if cycle % 500 == 0:
                print(f"Cycle: {cycle}")
            self.send_employed_bees()

            self.update_probabilities()

            self.send_onlooker_bees()

            self.memorize_best_food_sources()

            self.send_scout_bees()
            cycle += 1

        # self.best_food_sources[0].function_value()
        iteration_num = cycle
        exp_f = abs(self.best_food_sources[0].function_value() - 0)
        exp_x = abs(np.linalg.norm(np.array(self.best_food_sources[0].get_parameters()) - self._solution))
        return iteration_num, exp_f, exp_x

    def experiment3(self):
        best_food_source = None

        self.initialize_food_sources()
        self.memorize_best_food_sources()
        cycle = 0
        n_plus = 0
        while cycle < 1000:
            self.send_employed_bees()

            self.update_probabilities()

            self.send_onlooker_bees()

            self.memorize_best_food_sources()

            self.send_scout_bees()

            if abs(np.linalg.norm(np.array(self.best_food_sources[0].get_parameters()) - self._solution)) < self._eps:
                n_plus += 1

            cycle += 1

        # self.best_food_sources[0].function_value()
        success_p = n_plus / cycle
        exp_f = abs(self.best_food_sources[0].function_value() - 0)
        exp_x = abs(np.linalg.norm(np.array(self.best_food_sources[0].get_parameters()) - self._solution))
        return success_p, exp_f, exp_x

    def run(self) -> None:
        """
        Main function for algorithm.
        """
        best_food_source = None
        max_cycles = self._max_cycles

        self.initialize_food_sources()

        self.memorize_best_food_sources()
        for cycle in range(max_cycles):
            print(f"Cycle: {cycle}")
            self.send_employed_bees()

            self.update_probabilities()

            self.send_onlooker_bees()

            self.memorize_best_food_sources()

            self.send_scout_bees()

            for index, fs in enumerate(self.food_sources):
                fs.log_data(cycle, index)

            for index, fs in enumerate(self.best_food_sources):
                fs.log_best(cycle, index)
