from biosim.parameters import default_land_parameters_copy, default_animal_parameters_copy
from biosim.island import Island
import textwrap
import pytest


class TestFunctionsIsland:

    @pytest.fixture(autouse=True)
    def islands(self):
        geogr = """\
                        WWWWW
                        WLHDW
                        WWWWW"""

        geogr = textwrap.dedent(geogr)
        self.land_param = default_land_parameters_copy()
        self.animal_param = default_animal_parameters_copy()
        self.island = Island(geogr, self.land_param)
        self.population = [{'loc': (2, 2), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20}
                                                   for _ in range(50)]},
                           {'loc': (2, 2), 'pop': [{'species': 'Carnivore', 'age': 5, 'weight': 20}
                                                   for _ in range(20)]}]

    def test_not_island(self):
        with pytest.raises(ValueError):
            geogr = "H"
            Island(geogr, self.land_param)

    def test_invalid_island(self):
        with pytest.raises(ValueError):
            geogr = "WWW\nWLWW\nWWW"
            Island(geogr, self.land_param)

    def test_invalid_landtype(self):
        with pytest.raises(ValueError):
            geogr = "WWW\nWRW\nWWW"
            Island(geogr, self.land_param)

    def test_add_animal_to_water(self):
        population = [{'loc': (1, 1), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20}
                                              for _ in range(50)]}]
        with pytest.raises(ValueError):
            self.island.add_populations(population, self.animal_param)

    def test_add_population_out_of_bounds(self):
        population = [{'loc': (0, 1), 'pop': [{'species': 'Herbivore', 'age': 5, 'weight': 20}]}]
        with pytest.raises(ValueError):
            self.island.add_populations(population, self.animal_param)

    def test_all_animals_without_food(self):
        geogr = "WWWW\nWDDW\nWWWW"
        island = Island(geogr, self.land_param)
        island.add_populations(self.population, self.animal_param)
        for year in range(40):
            island.simulate_year()
        assert island.species_count('Herbivore') == 0
        assert island.species_count('Carnivore') == 0
