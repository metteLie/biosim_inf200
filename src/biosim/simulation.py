"""
Template for BioSim class.
"""

from .parameters import default_animal_parameters_copy, default_land_parameters_copy, \
    assert_valid_animal_parameter, assert_valid_land_parameter
import random
import logging
import sys
from .island import Island
from .biographics import BioGraphics

# The material in this file is licensed under the BSD 3-clause license
# https://opensource.org/licenses/BSD-3-Clause
# (C) Copyright 2021 Hans Ekkehard Plesser / NMBU


class BioSim:
    def __init__(self, island_map, ini_pop, seed,
                 vis_years=1, ymax_animals=None, cmax_animals=None, hist_specs=None,
                 img_dir=None, img_base=None, img_fmt='png', img_years=None,
                 log_file=None):
        """
        :param island_map: Multi-line string specifying island geography
        :param ini_pop: List of dictionaries specifying initial population, see ``add_population``.
        :param seed: used as random number seed
        :type seed: int
        :param log_file: If given, write animal counts to this file

        For the rest of parameters, see :ref:`biographics`.
        """
        self.seed = seed
        self.logger = logging.getLogger()
        self.logger.setLevel(logging.INFO)
        if log_file is not None:
            self.logger.addHandler(logging.FileHandler(log_file))
        else:
            self.logger.addHandler(logging.StreamHandler(sys.stdout))

        self.years_simulated = 0
        self.land_parameters = default_land_parameters_copy()
        self.animal_parameters = default_animal_parameters_copy()

        self.island = Island(island_map, self.land_parameters)
        self.add_population(ini_pop)

        self.graphing = BioGraphics(island_map, vis_years, ymax_animals, cmax_animals, hist_specs,
                                    img_dir, img_base, img_fmt, img_years)

    def set_animal_parameters(self, species, params):
        """
        Set parameters for animal species.

        :param species: String, name of animal species
        :param params: Dict with valid parameter specification for species

        Raises ``ValueError`` if parameters are unrecognized.
        For a list of recognized parameters, see :ref:`parameters`.
        """
        for param, value in params.items():
            assert_valid_animal_parameter(species, param, value)
            self.animal_parameters[species][param] = value

    def set_landscape_parameters(self, landscape, params):
        """
        Set parameters for landscape type.

        :param landscape: String, code letter for landscape
        :param params: Dict with valid parameter specification for landscape

        Raises ``ValueError`` if parameters are unrecognized.
        For a list of recognized parameters, see :ref:`parameters`.
        """
        for param, value in params.items():
            assert_valid_land_parameter(landscape, param, value)
            self.land_parameters[landscape][param] = value

    def simulate(self, num_years):
        """
        Run simulation while visualizing the result.

        :param num_years: number of years to simulate
        """
        random.seed(self.seed)

        self.graphing.setup(self.year + num_years)

        for year in range(num_years):
            self.island.simulate_year()
            self.years_simulated += 1
            self.graphing.update(self)

            self.logger.info(f"years: {self.year}, counts: {self.num_animals_per_species}")

    def add_population(self, population):
        """
        Add a population to the island

        :param population: List of dictionaries specifying population, see :ref:`island`.
        """
        self.island.add_populations(population, self.animal_parameters)

    @property
    def year(self):
        """ Last year simulated. """
        return self.years_simulated

    @property
    def num_animals(self):
        """ Total number of animals on island. """
        return sum(self.island.species_count(s) for s in self.animal_parameters.keys())

    @property
    def num_animals_per_species(self):
        """ Number of animals per species on the island, as a dictionary. """
        return {s: self.island.species_count(s) for s in self.animal_parameters.keys()}

    @property
    def num_animals_per_cell_per_species(self):
        """
        A dict with each species as keys.
        The values are dicts with the population of that species per (row,col) location.
        """
        return {s: self.island.cell_population(s) for s in self.animal_parameters.keys()}

    @property
    def fitness_per_species(self):
        """
        A dict containing one list per species, with all individuals' fitness values.
        """
        return {s: self.island.species_fitness(s) for s in self.animal_parameters.keys()}

    @property
    def ages_per_species(self):
        """
        A dict containing one list per species, with the ages of all members of the species.
        """
        return {s: self.island.species_ages(s) for s in self.animal_parameters.keys()}

    @property
    def weights_per_species(self):
        """
        A dict containing one list per species, with the weight of all members of the species.
        """
        return {s: self.island.species_weights(s) for s in self.animal_parameters.keys()}

    def make_movie(self):
        """ Create MPEG4 movie from visualization images saved. """
        self.graphing.make_movie()
