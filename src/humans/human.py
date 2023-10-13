from biosim.animals import Animal
import random


class Human(Animal):
    """ Class for a species of animal called carnivore """

    def __init__(self, age, weight, parameters):
        """
        :param age: Age of carnivore as an integer
        :param weight: Weight of carnivore as a float
        :param parameters: Dict with valid parameter specification for carnivores
        """
        super().__init__('Human', age, weight, parameters)

    @property
    def eating_priority(self):
        """
        See ``Animal.eating_priority``
        All humans (-2) eat in random order, after all carnivores (-1) and herbivores [0,1]
        """
        return -2

    # 1. feeding
    def feed(self, fodder, prey_list):
        """
        :param fodder: plant food available
        :param prey_list: list of preys for carnivores to eat

        See ``Animal.feed``.

        First tries to eat up to :math:`F_\\text{fodder}` fodder.
        If still hungry, starts hunting for prey.
        Unlike carnivore, it tries to eat the fittest prey first.
        Keeps trying until full (total food eaten reaches :math:`F`), or it has tried every prey.

        The chance of successfully killing and eating a given prey,
        is given by :math:`\\frac{\\Phi - \\Phi_\\text{prey}}{\\Delta\\Phi_\\text{max}}`.

        When consuming a unit of fodder, the body weight increases by :math:`\\beta_\\text{fodder}`.
        When consuming a unit of prey, the body weight increases by :math:`\\beta_\\text{prey}`.

        :returns: the amount of fodder eaten
        """
        # First eat up to F_fodder plants, if possible
        eaten_fodder = min(fodder, self.para['F_fodder'])
        eaten = eaten_fodder

        self.weight += self.para['beta_fodder'] * eaten_fodder

        # We possibly became full on fodder alone
        if eaten >= self.para['F']:
            return eaten_fodder

        # We always attempt to eat the weakest first
        prey_list.sort(key=lambda p: p.fitness)
        # Store our fitness locally, makes a significant speed difference
        own_fitness = self.fitness
        for prey in prey_list[::-1]:
            # No reason to continue once we reach dead prey
            if prey.weight <= 0:
                break

            relative_fitness = (own_fitness - prey.fitness)/self.para['DeltaPhiMax']
            if relative_fitness < 0:  # We have no shot at eating this prey
                continue
            if relative_fitness >= 1 or random.random() < relative_fitness:
                # Can not eat more than F
                eaten += (dinner := min(prey.weight, self.para['F']-eaten))
                prey.weight = 0  # Prey gets consumed upon eating
                self.weight += dinner * self.para['beta_prey']
                own_fitness = self.fitness
                if eaten >= self.para['F']:
                    break

        return eaten_fodder

    def try_give_birth(self, species_count):
        """
        :param species_count: A dict containing, for each species, \
        the number of members in this cell

        The human must be at least :math:`BirthAge_\\text{min}` to give birth.
        If satisfied, the formula from ``Animal`` is used to determine likelihood of birthing.
        See :ref:`animals`.

        :returns: the newborn human if a birth occurred, otherwise None
        """
        if self.age < self.para['BirthAge_min']:
            return
        return super().try_give_birth(species_count)
