from .landscape import Landscape


class Island:
    """
    Class representing an island of connected landscape cells, \
    with animals and simulation of years.
    """

    def __init__(self, landscape, land_parameters):
        """
        :param landscape: A multiline string of valid land_type chars, defining the island.
        :param land_parameters: A dict of parameters for each possible land_type char.

        The island map must be rectangular, and the border must consist of only the 'W' land type.
        Landscape cells are indexed as ``(row, col)``, with ``(1,1)`` being the upper left corner.
        """
        self._map = dict()
        self.land_parameters = land_parameters

        self._make_map(landscape)

    def _make_map(self, landscape):
        """ Uses the given landscape string to populate ``_map`` with instances of Landscape. """
        landscape = landscape.split()
        width = len(landscape[0])
        if any(cell != 'W' for cell in landscape[0] + landscape[-1]):
            raise ValueError("Not an island!")
        for i_row, row in enumerate(landscape):
            if len(row) != width:
                raise ValueError("Map rows have differing widths")
            if row[0] != 'W' or row[-1] != 'W':
                raise ValueError("Not an island!")
            for i_col, land_type in enumerate(row):
                loc = (i_row + 1, i_col + 1)
                self._map[loc] = Landscape(land_type, self.land_parameters)

    def add_populations(self, populations, parameters):
        """
        :param populations: A list of dictionaries with ``loc`` and ``pop`` as keys.
        :type populations: list
        :param parameters: A dict containing parameter dicts for each species

        Animals are placed in Landscape cells defined by the position, as ``(row, col)``.
        Population is a list of dictionaries fitting ``Landscape.add_population``,
        see :ref:`landscape`.
        """
        for population in populations:
            loc = population['loc']
            if loc not in self._map:
                raise ValueError(f'Illegal coordinate {loc}')
            self._map[loc].add_population(population['pop'], parameters)

    def species_count(self, species):
        """
        :param species: The species we want to count
        :returns: The total number of animals of the given species on the island.
        """
        return sum(cell.get_count_of_species(species) for cell in self._map.values())

    def cell_population(self, species):
        """
        :param species: The species we want to count.
        :returns: A dict with number of individuals of the given species for each cell location.
        """
        return {loc: cell.get_count_of_species(species) for loc, cell in self._map.items()}

    def species_fitness(self, species):
        """
        :param species: The species we want to list fitness of.
        :returns: A list of fitness for all animals of the given species on the island.
        """
        fitness = []
        for cell in self._map.values():
            fitness.extend(cell.species_fitness(species))
        return fitness

    def species_ages(self, species):
        """
        :param species: The species we want to list ages of.
        :returns: A list of ages for all animals of the given species on the island.
        """
        ages = []
        for cell in self._map.values():
            ages.extend(cell.species_ages(species))
        return ages

    def species_weights(self, species):
        """
        :param species: The species we want to list weights of.
        :returns: A list of weights for all animals of the given species on the island.
        """
        weights = []
        for cell in self._map.values():
            weights.extend(cell.species_weights(species))
        return weights

    def simulate_year(self):
        """
        Simulates one year on the island by iterating through each cell on island,
        and performing each step of the simulation. See the top of this document.
        """

        for (row, col), cell in self._map.items():
            cell.animal_feeding()
            cell.animal_breeding()
            # Migration requires references to neighbouring cells
            neighbours = [(row+1, col), (row, col+1), (row-1, col), (row, col-1)]
            valid_cells = [n for loc in neighbours if (n := self._map.get(loc, None)) is not None]
            cell.animal_migration(valid_cells)

        for cell in self._map.values():
            cell.finish_animal_migration()
            cell.animal_ageing()
            cell.animal_weight_loss()
            cell.animal_death()
