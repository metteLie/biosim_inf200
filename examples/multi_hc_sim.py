#! /usr/bin/env python

"""
Full island simulation with herbivores and carnivores at different locations in the beginning.
"""

import textwrap
from biosim.simulation import BioSim

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
                 {'loc': (10, 7),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(50)]},
                 {'loc': (7, 17),
                  'pop': [{'species': 'Herbivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(100)]}
                 ]

    ini_carns = [{'loc': (2, 7),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(50)]},
                 {'loc': (7, 16),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(50)]}
                 ]

    sim = BioSim(geogr, ini_herbs + ini_carns, seed=1,
                 hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                             'age': {'max': 60.0, 'delta': 2},
                             'weight': {'max': 60, 'delta': 2}},
                 cmax_animals={'Herbivore': 200, 'Carnivore': 50},
                 #img_dir='data',
                 img_base='sample')

    sim.simulate(200)
    #sim.make_movie()

    import matplotlib.pyplot as plt
    #plt.show()
