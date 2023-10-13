#! /usr/bin/env python

"""
Full island simulation with herbivores, carnivores and humans at different locations in the
beginning.
"""

import textwrap

from biosim.parameters import default_animal_parameters
from biosim.simulation import BioSim
from humans.parameters import default_human_parameters

if __name__ == '__main__':

    geogr = """\
               WWWWWWWWWWWWWWWWWWWWW
               WHHHHHLLLLWWLLLLLLLWW
               WHHHHHLLLLWWLLLLLLLWW
               WHHHHHLLLLWWLLLLLLLWW
               WWHHLLLLLLLWWLLLLLLLW
               WWHHLLLLLLLWWLLLLLLLW
               WWWWWWWWHWWWWLLLLLLLW
               WHHHHHLLLLWWLLLLLLLWW
               WHHHHHHHHHWWLLLLLLWWW
               WHHHHHDDDDDLLLLLLLWWW
               WHHHHHDDDDDLLLLLLLWWW
               WHHHHHDDDDDLLLLLLLWWW
               WHHHHHDDDDDWWLLLLLWWW
               WHHHHDDDDDDLLLLWWWWWW
               WWHHHHDDDDDDLWWWWWWWW
               WWHHHHDDDDDLLLWWWWWWW
               WHHHHHDDDDDLLLLLLLWWW
               WHHHHDDDDDDLLLLWWWWWW
               WWHHHHDDDDDLLLWWWWWWW
               WWWHHHHLLLLLLLWWWWWWW
               WWWHHHHHHWWWWWWWWWWWW
               WWWWWWWWWWWWWWWWWWWWW"""
    geogr = textwrap.dedent(geogr)

    ini_herbs = [{'loc': (2, 7),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(100)]},
                 {'loc': (7, 17),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(100)]}
                 ]

    ini_carns = [{'loc': (7, 16),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(50)]}
                 ]

    ini_humans = [{'loc': (4, 7),
                  'pop': [{'species': 'Human',
                           'age': 20,
                           'weight': 40}
                          for _ in range(50)]},
                 {'loc': (17, 5),
                  'pop': [{'species': 'Human',
                           'age': 20,
                           'weight': 40}
                          for _ in range(50)]}
                 ]

    default_animal_parameters.update(default_human_parameters)
    sim = BioSim(geogr, ini_herbs + ini_carns + ini_humans, seed=1,
                 hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                             'age': {'max': 60.0, 'delta': 2},
                             'weight': {'max': 60, 'delta': 2}},
                 cmax_animals={'Herbivore': 200, 'Carnivore': 50},
                 img_dir='data', img_years= 3,
                 img_base='sample')

    sim.simulate(200)
    sim.make_movie()

    import matplotlib.pyplot as plt
    plt.show()
