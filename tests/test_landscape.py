from biosim.parameters import default_animal_parameters_copy, default_land_parameters_copy
from biosim.landscape import Landscape
import pytest


class TestFunctionsLandscape:

    @pytest.fixture(autouse=True)
    def landscapes(self):
        self.para_land = default_land_parameters_copy()
        self.para_animal = default_animal_parameters_copy()

        self.water = Landscape('W', self.para_land)
        self.lowland = Landscape('L', self.para_land)
        self.dessert = Landscape('D', self.para_land)
        self.highland = Landscape('H', self.para_land)

        self.n_herbs = 20
        self.n_carns = 18
        self.ini_herbs = [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 25}
                          for _ in range(self.n_herbs)]
        self.ini_carns = [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 30}
                          for _ in range(self.n_carns)]

    def test_habitable(self):
        assert not self.water.habitable
        assert self.lowland.habitable
        assert self.dessert.habitable
        assert self.highland.habitable

    def test_add_population(self):
        self.highland.add_population(self.ini_herbs, self.para_animal)
        assert self.highland.animals is not None

    def test_add_illegal_animals(self):
        population = [{'species': 'Herbivore', 'age': -1, 'weight': 20}]
        with pytest.raises(ValueError):
            self.highland.add_population(population, self.para_animal)
        population = [{'species': 'Herbivore', 'age': 3, 'weight': 0}]
        with pytest.raises(ValueError):
            self.highland.add_population(population, self.para_animal)

    def test_count_species(self):
        self.highland.add_population(self.ini_herbs + self.ini_carns, self.para_animal)
        n_herbs = self.highland.get_count_of_species('Herbivore')
        n_carns = self.highland.get_count_of_species('Carnivore')
        assert n_herbs == self.n_herbs and n_carns == self.n_carns

    def test_animal_feeding(self):
        self.para_animal['Carnivore']['DeltaPhiMax'] = 0.01
        self.para_animal['Carnivore']['w_half'] = 0  # Great fitness among carnivores
        self.highland.add_population(self.ini_herbs + self.ini_carns, self.para_animal)
        self.highland.animal_feeding()
        n_herbs = self.highland.get_count_of_species('Herbivore')
        n_carns = self.highland.get_count_of_species('Carnivore')
        assert n_herbs < self.n_herbs
        assert n_carns == self.n_carns

    def test_animal_feeding_weightgain(self):
        """ Give a controlled amount of fodder in the cell, check the total animal weight gain """
        self.para_land['H']['f_max'] = 10.5 * self.para_animal['Herbivore']['F']
        self.highland.add_population(self.ini_herbs, self.para_animal)
        pre_weight = sum(self.highland.species_weights('Herbivore'))
        self.highland.animal_feeding()
        new_weight = sum(self.highland.species_weights('Herbivore'))
        gain_factor = self.para_land['H']['f_max'] * self.para_animal['Herbivore']['beta']
        assert new_weight == pytest.approx(pre_weight + gain_factor)

    def test_animal_breeding(self):
        """ With a high likelihood of breeding, check that the population increases """
        self.para_animal['Herbivore']['zeta'] = 1
        self.highland.add_population(self.ini_herbs, self.para_animal)
        start_animals = len(self.highland.animals)
        self.highland.animal_breeding()
        assert len(self.highland.animals) > start_animals

    def test_animal_ageing(self):
        self.highland.add_population(self.ini_herbs, self.para_animal)
        pre_sum_age = sum(self.highland.species_ages('Herbivore'))
        self.highland.animal_ageing()
        sum_age = sum(self.highland.species_ages('Herbivore'))
        assert sum_age == self.n_herbs + pre_sum_age

    def test_weight_loss(self):
        self.highland.add_population(self.ini_herbs, self.para_animal)
        pre_sum_weight = sum(self.highland.species_weights('Herbivore'))
        self.highland.animal_weight_loss()
        sum_weight = sum(self.highland.species_weights('Herbivore'))
        loss_factor = 1 - self.para_animal['Herbivore']['eta']
        assert sum_weight == pytest.approx(pre_sum_weight * loss_factor)

    def test_animal_death(self):
        self.highland.add_population([{'species': 'Herbivore', 'age': 50, 'weight': 0.1},  # unfit
                                      {'species': 'Herbivore', 'age': 0, 'weight': 300}],  # fit
                                     self.para_animal
                                     )
        # Chance of dying equal to omega*(1-fitness)
        self.para_animal['Herbivore']['omega'] = 1
        self.highland.animal_death()
        assert self.highland.get_count_of_species('Herbivore') == 1

    def test_animal_migration(self):
        self.para_animal['Herbivore']['mu'] = 1
        self.highland.add_population(self.ini_herbs, self.para_animal)
        self.highland.animal_migration([self.lowland, self.water])
        assert len(self.water.incoming_animals) == 0
        assert len(self.lowland.animals) == 0
        assert len(self.lowland.incoming_animals) > 0
        assert len(self.highland.animals + self.lowland.incoming_animals) == self.n_herbs

        self.lowland.finish_animal_migration()
        assert len(self.lowland.incoming_animals) == 0
        assert len(self.highland.animals + self.lowland.animals) == self.n_herbs
