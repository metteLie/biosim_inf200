from .animals import Animal
import random


class Carnivore(Animal):
    """ Class for a species of animal called carnivore """

    def __init__(self, age, weight, parameters):
        """
        :param age: Age of carnivore as an integer
        :param weight: Weight of carnivore as a float
        :param parameters: Dict with valid parameter specification for carnivores
        """
        super().__init__('Carnivore', age, weight, parameters)

    @property
    def eating_priority(self):
        """
        See ``Animal.eating_priority``.
        All carnivores (-1) eat in random order, after all herbivores [0,1]
        """
        return -1

    # 1. feeding
    def feed(self, fodder, prey_list):
        """
        :param fodder: plant food available
        :param prey_list: list of preys for carnivores to eat

        See ``Animal.feed``.

        The carnivore tries to eat the weakest prey first. Probability of eating is determined by
        difference in fitness:

        :math:`\\frac{\\Phi - \\Phi_\\text{prey}}{\\Delta\\Phi_\\text{max}}`.

        Eaten prey dies (weight = 0), and the carnivore gains weight.
        Per unit of prey consumed, the body weight increases by :math:`\\beta`.

        The carnivore stops hunting when full, and will not eat more than :math:`F` units of food.

        :returns: 0 since carnivores only eat prey, no fodder.
        """
        # Amount of weight eaten this year
        eaten = 0
        # We always attempt to eat the weakest first
        prey_list.sort(key=lambda p: p.fitness)
        # Store our fitness locally, makes a significant speed difference
        own_fitness = self.fitness
        for prey in prey_list:
            # Skip trying to eat dead animals
            if prey.weight <= 0:
                continue

            relative_fitness = (own_fitness - prey.fitness)/self.para['DeltaPhiMax']
            if relative_fitness < 0:  # We have no shot at eating this prey, or any following
                break
            if relative_fitness >= 1 or random.random() < relative_fitness:
                # Can not eat more than F
                eaten += (dinner := min(prey.weight, self.para['F']-eaten))
                prey.weight = 0  # Prey gets consumed upon eating
                self.weight += dinner * self.para['beta']
                own_fitness = self.fitness
                if eaten >= self.para['F']:
                    break

        return 0  # We didn't eat any fodder
