import random
from collections import Counter


class Landscape:
    """
    Represents single cell of the :ref:`island`, \
    containing the :ref:`animals` currently residing there.
    """
    def __init__(self, land_type, param):
        """
        :param land_type: Character specifying type of land
        :param param: A dict containing parameters for each type of land
        """
        self.param = param
        self.land_type = land_type

        if land_type not in param:
            raise ValueError("Unrecognized land type")

        self.animals = []
        self.incoming_animals = []

    @property
    def habitable(self):
        """ :returns: True if land type is habitable, and False if not habitable. """
        return self.param[self.land_type]['habitable']

    def add_population(self, population, param):
        """
        :param population: List of dictionaries with species, age and weight as keys.
        :param param: Dict of animal parameters, that contains parameters for all species.

        Constructs all given animals and stores them in the landscape object.
        """
        for a in population:
            if not self.habitable:
                raise ValueError("Can't add species to non-habitable landscape")
            species = a['species']
            new_animal = param[species]['constructor'](a['age'], a['weight'], param[species])
            self.animals.append(new_animal)

    def get_count_of_species(self, species):
        """
        :param species: Name of one species.
        :type species: str

        Counts number of animals that belong to the given species.

        :returns: Number of animals of the given species.
        """
        return sum(a.species == species for a in self.animals)

    def species_fitness(self, species):
        return [a.fitness for a in self.animals if a.species == species]

    def species_ages(self, species):
        return [a.age for a in self.animals if a.species == species]

    def species_weights(self, species):
        return [a.weight for a in self.animals if a.species == species]

    def animal_feeding(self):
        """
        All animals in cell eat in priority order (high to low). Priority order is
        given as fitness for herbivores, the fittest eats first. All carnivores have
        priority -1, to eat in random order, but after all herbivores.

        All animals have the opportunity to eat fodder, but carnivores choose not to.
        The cell has a limited amount of fodder, given as the ``f_max`` parameter.
        See details in :ref:`herbivore` and :ref:`carnivore`.

        Preys that are eaten, are removed from the list of animals in the cell.
        """
        # Plant food
        fodder = self.param[self.land_type]['f_max']

        # First shuffle animals to give random order, then sort by priority
        random.shuffle(self.animals)
        self.animals.sort(key=lambda a: a.eating_priority, reverse=True)

        # List of prey in the landscape
        prey = [a for a in self.animals if a.is_prey]

        # Let each animal eat in turn, giving access to both plants and prey
        for animal in self.animals:
            fodder -= animal.feed(fodder, prey)

        # Remove all animals that were eaten
        self.animals = [a for a in self.animals if a.weight > 0]

    def animal_breeding(self):
        """
        Animals can try to give birth if there are other animals of the same
        species in the same landscape-cell. For all the successful births,
        the newborns are added to the list of animals.

        A newborn does not contribute to the species count until breeding is finished.
        """
        species_count = Counter(a.species for a in self.animals)

        new_animals = []
        for a in self.animals:
            if (child := a.try_give_birth(species_count)) is not None:
                new_animals.append(child)
        self.animals.extend(new_animals)

    def animal_ageing(self):
        """ All animals get one year older. """
        for a in self.animals:
            a.ageing()

    def animal_weight_loss(self):
        """ All animals lose weight, call once per year """
        for a in self.animals:
            a.weight_loss()

    def animal_death(self):
        """
        Checks each animal if it happens to die this year. If so, removes it. See :ref:`animals`.
        """
        self.animals = [a for a in self.animals if not a.death()]

    def animal_migration(self, neighbour_cells):
        """
        :param neighbour_cells: Landscape-cells north, west, east and south from \
        current landscape-cell.

        Tries to migrate animals in this landscape-cell.
        Animals that cannot move, or choose not to, will stay.
        Moving animals leave ``animals``, and enter the target cell's ``ìncoming_animals``.
        This lets the incoming cell finish early simulation phases without the incoming animals.
        See ``finish_animal_migration``.
        """
        self.animals = [a for a in self.animals if not a.try_migrate(neighbour_cells)]

    def try_accept_migrating_animal(self, animal):
        """
        :param animal: Animal object.

        Checks if this cell is habitable for the animal.
        If the cell is habitable, then the animal will be placed in ``incoming_animals``.
        True is returned, to let the caller know that the animal is now moved,
        and should be removed from its previous ``animals`` list.

        :returns: True if this cell is habitable, and now has the animal
        """
        if not self.habitable:
            return False
        self.incoming_animals.append(animal)
        return True

    def finish_animal_migration(self):
        """
        After all animals on the island have tried to migrate, the ones who
        succeeded will be removed from their old, and registered in their new landscape cells.
        This method moves the newcomers from ``incoming_animals`` into the ``animals``-list,
        making the new animals take part in all future simulation-steps on this cell.
        """
        self.animals.extend(self.incoming_animals)
        self.incoming_animals.clear()
