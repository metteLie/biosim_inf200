"""
Tests for animals
"""
import pytest
import random
from biosim.herbivore import Herbivore
from biosim.carnivore import Carnivore
from biosim.parameters import default_animal_parameters_copy, default_land_parameters_copy
from biosim.landscape import Landscape


class TestFunctionsAnimals:

    @pytest.fixture(autouse=True)
    def create_animals(self):
        self.parameters = default_animal_parameters_copy()
        self.land_params = default_land_parameters_copy()

        self.para_herb = self.parameters['Herbivore']
        self.herbivore = Herbivore(5, 40, self.para_herb)

        self.para_carn = self.parameters['Carnivore']
        self.carnivore = Carnivore(5, 40, self.para_carn)

        self.animals = {'Herbivore': self.herbivore, 'Carnivore': self.carnivore}

    @pytest.mark.parametrize('animal_type',
                             ['Herbivore', 'Carnivore'])
    def test_create_illegal_animal(self, animal_type):
        # Create animal with negative age
        with pytest.raises(ValueError):
            self.parameters[animal_type]['constructor'](-1, 10, self.parameters[animal_type])
        # Create animal with 0 weight
        with pytest.raises(ValueError):
            self.parameters[animal_type]['constructor'](4, 0, self.parameters[animal_type])

    # fitness
    @pytest.mark.parametrize('animal_type',
                             ['Herbivore', 'Carnivore'])
    def test_fitness(self, animal_type):
        animal = self.animals[animal_type]
        animal.para['phi_weight'] = 0
        animal.para['phi_age'] = 0
        assert animal.fitness == 1/4

    @pytest.mark.parametrize('animal_type',
                             ['Herbivore', 'Carnivore'])
    def test_fitness_changing(self, animal_type):
        animal = self.animals[animal_type]
        # 00 is a bitstring of (delta_weight, delta_age)
        fitness00 = animal.fitness
        animal.weight += 1  # More weight gives higher fitness
        assert (fitness10 := animal.fitness) > fitness00
        animal.age += 1  # Older gives lower fitness
        assert (fitness11 := animal.fitness) < fitness10
        animal.weight -= 1
        fitness01 = animal.fitness
        assert fitness00 > fitness01 < fitness11

    @pytest.mark.parametrize('animal_type',
                             ['Herbivore', 'Carnivore'])
    def test_fitness_zero_weight(self, animal_type):
        animal = self.parameters[animal_type]['constructor'](5, 5, self.parameters[animal_type])
        animal.weight = 0
        assert animal.fitness == 0

    # feeding
    def test_herbivore_feeding(self):
        fodder = 30
        old_weight = self.herbivore.weight
        eat = self.herbivore.feed(fodder, [])
        assert self.herbivore.weight - old_weight == self.para_herb['beta']*eat

    def test_carnivore_feeding_grass(self):
        fodder = 30
        old_weight = self.carnivore.weight
        assert self.carnivore.feed(fodder, []) == 0
        assert self.carnivore.weight == old_weight

    def test_weak_carnivore_vs_prey(self):
        # Make him weak
        self.carnivore.weight = 1
        self.carnivore.age = 100

        # Make the prey strong enough to have chance of being eaten = 0
        self.herbivore.weight = 100
        self.herbivore.age = 1

        for _ in range(1000):
            self.carnivore.feed(0, [self.herbivore])
            assert self.herbivore.weight != 0  # Has not been eaten

    def test_carnivore_not_eat_dead_prey(self):
        # Make the prey dead
        old_weight = self.carnivore.weight
        self.herbivore.weight = 0
        self.carnivore.feed(0, [self.herbivore])
        assert old_weight == self.carnivore.weight

    @pytest.mark.parametrize('max_eat',
                             [10, 2])
    def test_carnivore_killing(self, max_eat):
        """
        Tests that eating an animal kills it and increases weight.
        Also tests with limited stomach
        """
        self.carnivore.weight = (start_weight := 100)
        self.herbivore.weight = (prey_weight := 5)

        # Make sure we always succeed in killing
        assert self.carnivore.fitness - self.herbivore.fitness > 0.01
        self.para_carn['DeltaPhiMax'] = 0.01

        self.para_carn['F'] = max_eat
        self.carnivore.feed(0, [self.herbivore])
        assert self.herbivore.weight == 0

        eaten = min(max_eat, prey_weight)
        assert self.carnivore.weight == start_weight + self.para_carn['beta'] * eaten

    def test_carnivore_feed_multiple_prey(self):
        """
        Creates a pack of very old (low fitness) prey.
        Checks that a carnivore eats the weakest first, until it it full.
        """
        prey = [Herbivore(100, weight, self.para_herb) for weight in range(10, 40)]
        self.para_carn['DeltaPhiMax'] = 0.01  # We always win our encounters

        random.shuffle(prey)
        self.para_carn['F'] = 30  # Will be able to eat the herbs weighing 10, 11 and 12
        self.carnivore.feed(0, prey)

        # Now, only prey weighing more than 12 should be alive
        for p in prey:
            assert p.weight == 0 or p.weight > 12
        assert sum(p.weight == 0 for p in prey) == 3

    # procreation
    def test_procreation(self):
        ini_herb = [Herbivore(5, 40, self.para_herb) for _ in range(10)]
        # A Herbivore must weight at least 33.25 to give birth

        # Makes fitness = 1/4 for all
        self.para_herb['phi_weight'] = 0
        self.para_herb['phi_age'] = 0

        self.para_herb['gamma'] = 0.1111
        # Gives a total P of giving birth ~0.25

        species_count = {'Herbivore': len(ini_herb)}
        new_herb = [c for h in ini_herb if (c := h.try_give_birth(species_count)) is not None]
        # Assert we got at least one child, but not all
        assert len(ini_herb) > len(new_herb) > 0

    def test_birth_weight(self):
        # Pop 1000 makes birth guaranteed
        pop = 1000
        self.herbivore.weight = (parent_weight := 40)
        child = self.herbivore.try_give_birth({'Herbivore': pop})
        assert child is not None
        assert parent_weight - child.weight * self.para_herb['xi'] == self.herbivore.weight

    def test_low_motherweight(self):
        pop = 1000
        self.para_herb['w_birth'] = 40
        assert self.herbivore.try_give_birth({'Herbivore': pop}) is None

    # migration
    @pytest.mark.parametrize('land_type',
                             ['L', 'H', 'D', 'W'])
    def test_animals_migration(self, land_type):
        cell = Landscape(land_type, self.land_params)
        water = Landscape('W', self.land_params)

        self.para_herb['mu'] = 1
        for _ in range(20):
            if self.herbivore.try_migrate([cell, water]):
                assert cell.habitable and self.herbivore in cell.incoming_animals
                return

        assert not cell.habitable

    def test_unfit_to_migrate(self):
        """ Creates a very unfit carnivore, it will be extremely unlikely to migrate """
        cell = Landscape('L', self.land_params)
        self.carnivore.weight = 1
        self.carnivore.age = 100
        for _ in range(20):
            assert not self.carnivore.try_migrate([cell])
        assert self.carnivore not in cell.incoming_animals

    # ageing
    def test_ageing(self):
        num_years = 5
        previous_age = self.herbivore.age
        for year in range(num_years):
            self.herbivore.ageing()
        assert self.herbivore.age == previous_age + num_years

    # loss of weight
    def test_weight_loss(self):
        old_weight = self.herbivore.weight
        self.herbivore.weight_loss()
        new_weight = self.herbivore.weight
        assert old_weight - new_weight == pytest.approx(self.para_herb['eta']*old_weight)

    # death
    def test_certain_death(self):
        herbivore = Herbivore(5, 5, self.para_herb)
        herbivore.weight = 0
        assert herbivore.death()

    def test_probable_death(self):
        """ Statistical: At least half should die, but not all """
        # Makes fitness = 1/4 for all
        self.para_herb['phi_weight'] = 0
        self.para_herb['phi_age'] = 0
        # Chance of death: omega * (1-fitness)
        self.para_herb['omega'] = 1
        ini_herb = [Herbivore(5, 20, self.para_herb) for _ in range(100)]
        survivors = [h for h in ini_herb if not h.death()]
        # Probability of death is 0.75
        # We assert that at least half die, but not all
        assert len(ini_herb) / 2 > len(survivors) > 0

    def test_no_death(self):
        """ With no chance of dying, we never die """
        self.para_herb['omega'] = 0
        for _ in range(1000):
            assert not self.herbivore.death()
