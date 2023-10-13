"""
Tests for humans
"""

import pytest
from humans.human import Human
from humans.parameters import default_human_parameters
from biosim.herbivore import Herbivore
from biosim.parameters import default_animal_parameters


class TestFunctionsHuman:

    @pytest.fixture(autouse=True)
    def create_animals(self):
        self.para_human = default_human_parameters['Human'].copy()
        self.human = Human(20, 50, self.para_human)

        self.para_herb = default_animal_parameters['Herbivore'].copy()
        self.herbivore = Herbivore(5, 40, self.para_herb)

    def test_no_fertile_children(self):
        n_humans = {'Human': 1000}  # Very likely for human to give birth
        human = Human(self.para_human['BirthAge_min']-1, 50, self.para_human)
        assert human.try_give_birth(n_humans) is None
        human.age += 1
        assert human.try_give_birth(n_humans) is not None

    def test_human_eats_prey(self):
        self.herbivore.age = 100  # prey with low fitness
        self.herbivore.weight = 5
        old_weight = self.human.weight
        self.para_human['DeltaPhiMax'] = 0.5  # Be sure we overpower the prey
        self.human.feed(0, [self.herbivore])
        assert self.human.weight == pytest.approx(old_weight + self.para_human['beta_prey']*5)

    @pytest.mark.parametrize('fodder', [5, 100])
    def test_human_eats_fodder(self, fodder):
        # Tries eating fodder, both with a scarce and huge amount available
        self.para_human['F_fodder'] = 20
        old_weight = self.human.weight
        eaten = self.human.feed(fodder, [])
        assert self.human.weight == old_weight + eaten * self.para_human['beta_fodder']
        assert eaten == min(self.para_human['F_fodder'], fodder)
