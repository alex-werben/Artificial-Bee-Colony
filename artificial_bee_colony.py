from food_source import FoodSource
import numpy as np
import random

class ArtificialBeeColony:
    def __init__(self, max_iterations_, max_food_sources_):
        self.best_food_source = None  # best source so far
        self.max_iterations = max_iterations_
        self.max_food_sources = max_food_sources_
        self.food_sources = []

    def get_new_based_on(self, food_source: FoodSource, fs_num: int) -> FoodSource:
        """

        :param food_source:
        :param fs_num:
        :return: new FoodSource
        """
        fs_count = self.max_food_sources
        neighbor_fs_num = random.randint(0,)

        pass

    def initialize_food_sources(self) -> None:
        """
        Setup random food sources.
        """
        for food_source_num in range(self.max_food_sources):
            self.food_sources.append(FoodSource())

    def send_employed_bees(self):
        """
        Send in employed bees for food.
        Employed bees return with nectar.
        """
        for fs_num in range(len(self.food_sources)):
            new_food_source = self.get_new_based_on(self.food_sources[fs_num])

            if self.food_sources[fs_num].nectar < new_food_source.nectar:
                self.food_sources[fs_num] = new_food_source
            else:
                self.food_sources[fs_num].trial_count += 1

    def update_probabilities(self):
        """
        Update desirability of food sources.
        Onlooker bees will now pick food source and
        explore the neighborhood, replacing with better
        food sources when found
        """
        pass

    def send_onlooker_bees(self):
        pass

    def memorize_best_food_sources(self):
        """
        Memorize the best food source for this cycle.
        """
        pass

    def send_scout_bees(self):
        pass

    def run(self):
        """
        Main function for algorithm.
        """
        pass
