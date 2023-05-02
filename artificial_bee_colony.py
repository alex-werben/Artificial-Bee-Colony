from food_source import FoodSource
import numpy as np
import random

class ArtificialBeeColony:
    def __init__(self, max_iterations_, max_food_sources_):
        self.best_food_sources = None  # best source so far
        self.max_iterations = max_iterations_
        self.max_food_sources = max_food_sources_
        self.food_sources = []
        self._scout_limit = 0
        self.num_solutions = 1

    def get_scout_limit(self):
        return self._scout_limit

    def get_new_based_on(self, food_source: FoodSource, fs_num: int) -> FoodSource:
        """

        :param food_source:
        :param fs_num:
        :return: new FoodSource
        """
        fs_count = self.max_food_sources
        neighbor_fs_num = np.random.randint(0, fs_count - 1)

        # to eliminate picking itself
        if neighbor_fs_num == fs_num:
            neighbor_fs_num += 1

        new_food_source = food_source.get_neighboring(self.food_sources[neighbor_fs_num])

        return new_food_source

    def generate_new_food_source(self) -> FoodSource:
        return FoodSource()

    def initialize_food_sources(self) -> None:
        """
        Setup random food sources.
        """
        for food_source_num in range(self.max_food_sources):
            self.food_sources.append(FoodSource())

    def send_employed_bees(self) -> None:
        """
        Send in employed bees for food.
        Employed bees return with nectar.
        """
        for fs_num in range(len(self.food_sources)):
            new_food_source = self.get_new_based_on(self.food_sources[fs_num])

            if self.food_sources[fs_num].get_nectar() < new_food_source.get_nectar():
                self.food_sources[fs_num] = new_food_source
            else:
                self.food_sources[fs_num].increment_trial_count()

    def update_probabilities(self):
        """
        Update desirability of food sources.
        Onlooker bees will now pick food source and
        explore the neighborhood, replacing with better
        food sources when found
        """
        pass

    def send_onlooker_bees(self) -> None:
        """
        Onlooker bee perceives the amount of nectar
        that each employed bee got from its food
        source with some error.
        Onlooker bee picks food source, from which
        more nectar was brought.
        """
        onlookers = self.max_food_sources

        for onlooker in range(onlookers):
            r = np.random.uniform(0, 1)
            prop_sum = 0

            for fs_num, food_source in enumerate(self.food_sources):
                prop_sum += food_source.get_probability()

                if r <= prop_sum:
                    new_food_source = self.get_new_based_on(food_source, fs_num)

                    if food_source.get_nectar() < new_food_source.get_nectar():
                        self.food_sources[fs_num] = new_food_source
                    else:
                        food_source.increment_trial_count()
                    break

    def memorize_best_food_sources(self):
        """
        Memorize the best food source for this cycle.
        """
        food_sources_map = {}
        for food_source in self.food_sources:
            if not food_sources_map.get(food_source.get_id()):
                food_sources_map[food_source.get_id()] = food_source
            else:
                if food_sources_map[food_source.get_id()].get_nectar() < food_source.get_nectar():
                    food_sources_map[food_source.get_id()] = food_source

        unique_food_sources = list(food_sources_map.values())
        unique_food_sources.sort()

        self.best_food_sources = unique_food_sources[:self.num_solutions]
        for fs in self.best_food_sources:
            fs.reset_trial_count()

    def send_scout_bees(self) -> None:
        """
        Scouts find random new food sources which
        may be either better or worse than the old one.
        """
        scout_limit = self.get_scout_limit()

        max_trial_fs = self.food_sources[0]
        max_trial_fs_num = 0
        for fs_num, food_source in enumerate(self.food_sources):
            if food_source.get_trial_count() > max_trial_fs.get_trial_count():
                max_trial_fs = food_source
                max_trial_fs_num = fs_num

        if max_trial_fs.get_trial_count() > scout_limit:
            new_food_source = self.generate_new_food_source()
            self.food_sources[max_trial_fs_num] = new_food_source

    def run(self):
        """
        Main function for algorithm.
        """

        pass
