.. _biosim:

BioSim
==================================

``BioSim`` simulates an island with landscape that contains animals and fodder. It also contains
methods to get information to pass to the graphics. This class is the entry point to simulating
with the ``biosim`` module. See the ``examples/`` folder for usage examples.

The following constructor is taken from ``complete_example.py``.::

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

.. autoclass:: biosim.simulation.BioSim
   :members:
