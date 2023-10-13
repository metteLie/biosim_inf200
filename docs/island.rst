.. _island:

Island
==================================
The island contains the grid of landscape cells.
The map must be rectangular and surrounded by water cells.
The island maps locations to cells, but the cells themselves do not know their own location.
Methods provide summary information about the animals on the island.
``simulate_year`` simulates one year, with all 6 seasons, on all cells.
Animal migration is synchronized to ensure each animal only experiences each season once per year.

.. autoclass:: biosim.island.Island
   :members:
