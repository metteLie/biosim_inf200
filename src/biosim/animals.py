import random
import math


class Animal:
    """
    Abstract class representing an animal.
    Has methods for simulating the different phases of the year, see the :ref:`front page<index>`.
    """

    def __init__(self, species, age, weight, parameters):
        """
        :param species: Name of the species
        :type species: str
        :param age: Age of animal
        :type age: int
        :param weight: Weight of animal
        :type weight: float
        :param parameters: Valid parameter specification for the given species
        :type parameters: dict
        """
        if age < 0 or weight <= 0:
            raise ValueError("Invalid starting conditions of an animal")

        self.species = species
        self._age = age
        self._weight = weight
        self._calculated_fitness = None
        self.para = parameters

    @property
    def fitness(self):
        """
        Calculates the fitness (:math:`\\Phi`) of the animal, based on weight and age.

        :math:`p_\\text{age} = \\frac{1}{1+\\exp(\\phi_\\text{age}(age - age_\\text{half}))}`

        :math:`p_\\text{weight} =
        \\frac{1}{1+\\exp(-\\phi_\\text{weight}(weight - weight_\\text{half}))}`

        :math:`\\Phi = p_\\text{age} p_\\text{weight}`
        """
        # Only calculates fitness if age or weight has changed
        if self._calculated_fitness is None:
            if self._weight <= 0:
                self._calculated_fitness = 0
            else:
                exp_age = self.para['phi_age'] * (self._age - self.para['a_half'])
                exp_weight = -self.para['phi_weight'] * (self._weight - self.para['w_half'])
                q_plus = 1 / (1 + math.exp(exp_age))
                q_minus = 1 / (1 + math.exp(exp_weight))
                self._calculated_fitness = q_plus * q_minus
        return self._calculated_fitness

    @property
    def eating_priority(self):
        """
        During the eating phase, animals are ordered by decreasing eating priority.
        For identical priorities, the order is random
        """
        raise NotImplementedError

    @property
    def is_prey(self):
        """ Determines if the animal can be eaten by other animals """
        return self.para['prey']

    # 1. feeding
    def feed(self, fodder, prey_list):
        """
        :param fodder: The amount of plant fodder available to eat
        :param prey_list: A list of all prey animals in the cell

        :returns: the amount of fodder consumed

        Any consumed prey must be informed, by setting its weight to zero.
        """
        raise NotImplementedError

    # 2. procreation
    def try_give_birth(self, species_count):
        """
        :param species_count: Number of individuals of each species at start of procreation

        Animal tries to give birth. Must fit minimum weight criteria:

        :math:`w \\geq \\zeta(w_\\text{birth} + \\sigma_\\text{birth})`

        If satisfied, the probability of giving birth is proportional to own fitness,
        as well as the number of other animals of the same species (N - 1):

        :math:`p_ = \\gamma \\Phi (N-1)`

        If giving birth, the new child is an animal of the same species with age zero.
        The weight of the new child is randomly sampled, following:

        :math:`w_\\text{child} \\sim N(w_\\text{birth},\\sigma_\\text{birth})`

        giving the parent a proportional weight loss:

        :math:`\\Delta w = -\\xi w_\\text{child}`

        .. note::
           If the sampled weight is so large that the parent would end up with negative weight,
           the birth is aborted

        :returns: None if no child was born, returns the child if one is born
        """

        # We need to be heavy enough to give birth
        if self.weight < self.para['zeta']*(self.para['w_birth'] + self.para['sigma_birth']):
            return None

        p = min(1.0, self.para['gamma'] * self.fitness * (species_count[self.species] - 1))
        if random.random() > p:  # Probability 1-p of not giving birth
            return None

        # We lose more weight than just the weight of the child
        birth_weight = random.gauss(self.para['w_birth'], self.para['sigma_birth'])
        wight_loss = self.para['xi'] * birth_weight
        if wight_loss < self.weight:
            self.weight -= wight_loss
            return self.para['constructor'](0, birth_weight, self.para)

    # 3. migration
    def try_migrate(self, neighbour_cells):
        """
        :param neighbour_cells: A list of all four neighbour Landscape cells (must not be empty)

        Tries to move to a neighbouring cell.
        The chance of migration is proportional to fitness, as well as random chance:

        :math:`p_\\text{migrate} = \\mu\\Phi`

        If the animal tries to migrate, it picks a neighbour cell at random (equal probability)
        even if one or more neighbours are not habitable.
        Returns True if animal successfully migrated, and should no longer reside in its original \
        cell.
        """
        if random.random() < self.para['mu']*self.fitness:
            return random.choice(neighbour_cells).try_accept_migrating_animal(self)
        return False

    # 4. ageing
    def ageing(self):
        """ Increases age of animal by 1. """
        self.age += 1

    # 5. loss of weight
    def weight_loss(self):
        """
        Each year the animal loses weight proportional to its current weight.

        :math:`\\Delta \\text{weight} = -\\eta \\text{weight}`

        Call once per year.
        """
        self.weight -= self.para['eta'] * self.weight

    # 6. death
    def death(self):
        """
        If the animals weight is zero or is unlucky, it dies.
        Chance of death is proportional to (1 - fitness):

        :math:`p_\\text{death} = \\omega (1 - \\Phi)`

        Call once per year, during the death phase.

        :returns: True if dead
        """
        return self.weight <= 0 or random.random() < self.para['omega']*(1.0 - self.fitness)

    # Properties used to dirty the calculated fitness value upon changes
    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, new_weight):
        self._weight = new_weight
        self._calculated_fitness = None

    @property
    def age(self):
        return self._age

    @age.setter
    def age(self, new_age):
        self._age = new_age
        self._calculated_fitness = None
