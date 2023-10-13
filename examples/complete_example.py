#! /usr/bin/env python

"""
Full island simulation with herbivores and carnivores.
Modified to showcase all BioSim parameters
"""

__author__ = 'Hans Ekkehard Plesser, NMBU'

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
                          for _ in range(200)]}]
    ini_carns = [{'loc': (2, 7),
                  'pop': [{'species': 'Carnivore',
                           'age': 5,
                           'weight': 20}
                          for _ in range(50)]}]

    sim = BioSim(geogr, ini_herbs + ini_carns, seed=1,
                 # Configure bin range and size for histograms
                 hist_specs={'fitness': {'max': 1.0, 'delta': 0.05},
                             'age': {'max': 60.0, 'delta': 2},
                             'weight': {'max': 60, 'delta': 2}},

                 # Configure max color ranges for the species heatmaps
                 cmax_animals={'Herbivore': 200, 'Carnivore': 50},

                 # To only visualize every 4th year (0 to fully disable)
                 # vis_years=4

                 # To enable saving an image every 8 years
                 # img_dir='data', img_base='sample', img_fmt='png', img_years=8

                 # To write species counts to a file instead of to stdout
                 # log_file='biosim.log'
                 )

    # To change stomach size of all Herbivores
    # sim.set_animal_parameters('Herbivore', {'F': 20})

    # To place more fodder in lowlands every year
    # sim.set_landscape_parameters('L', {'f_max': 1000})

    sim.simulate(num_years=200)

    # Call if image saving was enabled, to merge images to a video
    # sim.make_movie()

