from .animals import Animal


class Herbivore(Animal):
    """ Class for a species of animal called herbivore """

    def __init__(self, age, weight, parameters):
        """
        :param age: Age of herbivore as an integer
        :param weight: Weight of herbivore as a float
        :param parameters: Dict with valid parameter specification for herbivores
        """
        super().__init__('Herbivore', age, weight, parameters)

    @property
    def eating_priority(self):
        """
        See ``Animal.eating_priority``.
        The fittest herbivores eat first.
        """
        return self.fitness

    # 1. feeding
    def feed(self, fodder, prey_list):
        """
        :param fodder: The amount of plant fodder left in our landscape
        :param prey_list: List of prey in our landscape, we don't eat them

        The herbivore will eat until there is no more fodder, or it has eaten :math:`F`.
        After eating, the body weight increases by
        :math:`\\beta` times the amount of fodder it consumed.

        :returns: Amount of fodder eaten
        """
        eat = min(fodder, self.para['F'])  # Can only eat up to F
        self.weight += eat * self.para['beta']
        return eat
