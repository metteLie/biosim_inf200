from .herbivore import Herbivore
from .carnivore import Carnivore


default_animal_parameters = {
    'Herbivore': {
        'w_birth': 8.,
        'sigma_birth': 1.5,
        'beta': 0.9,
        'eta': 0.05,
        'a_half': 40.,
        'phi_age': 0.6,
        'w_half': 10.,
        'phi_weight': 0.1,
        'mu': 0.25,
        'gamma': 0.2,
        'zeta': 3.5,
        'xi': 1.2,
        'omega': 0.4,
        'F': 10.,
        'prey': True,
        'constructor': Herbivore
    },
    'Carnivore': {
        'w_birth': 6.,
        'sigma_birth': 1.,
        'beta': 0.75,
        'eta': 0.125,
        'a_half': 40.,
        'phi_age': 0.3,
        'w_half': 4.,
        'phi_weight': 0.4,
        'mu': 0.4,
        'gamma': 0.8,
        'zeta': 3.5,
        'xi': 1.1,
        'omega': 0.8,
        'F': 50.,
        'DeltaPhiMax': 10.,
        'prey': False,
        'constructor': Carnivore
    }
}


# Upper limit on beta added by us (should not gain more weight than eaten).
max_1_animal_params = ['beta', 'eta']
non_numeric_animal_params = ['prey', 'constructor']

default_land_parameters = {
    'L': {'f_max': 800, 'habitable': True},
    'H': {'f_max': 300, 'habitable': True},
    'D': {'f_max': 0, 'habitable': True},
    'W': {'f_max': 0, 'habitable': False}
}
non_numeric_land_params = ['habitable']


def default_animal_parameters_copy():
    """ Creates a deep copy of the default animal parameters """
    return {species: value.copy() for species, value in default_animal_parameters.items()}


def default_land_parameters_copy():
    """ Creates a deep copy of the default land parameters """
    return {landtype: value.copy() for landtype, value in default_land_parameters.items()}


def assert_valid_animal_parameter(species, param, value):
    """
    :param species: Name of species
    :param param: Name of the parameter
    :param value: User specified parameter value

    Checks if user specified parameter is valid for the species.
    The parameter must be recognized, and values must be in valid range.
    Raises ``ValueError`` if checks fail.
    """
    if species not in default_animal_parameters:
        raise ValueError(f'Unknown species {species}')
    if param not in default_animal_parameters[species]:
        raise ValueError(f'Unknown parameter {param}')
    if param in non_numeric_animal_params:
        return
    if value < 0:
        raise ValueError(f'{param} can not be negative')
    if param in max_1_animal_params and value > 1:
        raise ValueError(f'{param} can not be more than 1')
    if param == 'DeltaPhiMax' and value <= 0:
        raise ValueError(f'{param} must be a positive value')


def assert_valid_land_parameter(landscape, param, value):
    """
    :param landscape: Letter representing landscape type
    :param param: Name of the parameter
    :param value: User specified parameter value

    Checks if user specified parameter is valid for the landscape.
    The parameter must be recognized, and values must be in valid range.
    Raises ``ValueError`` if checks fail.
    """
    if landscape not in default_land_parameters:
        raise ValueError(f'Unknown landscape {landscape}')
    if param not in default_land_parameters[landscape]:
        raise ValueError(f'Unknown parameter {param}')
    if param in non_numeric_land_params:
        return
    if value < 0:
        raise ValueError(f'{param} can not be negative')
