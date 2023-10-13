.. _landscape:

Landscape
==================================

The ``Landscape`` objects are made from ``Island``, where it gets its land-type, parameters and
animals. The animals are stored in a list and the land-type decides how much fodder that is
available for the cell each year.

When ``Island`` simulates a year, it calls on methods from landscape. The landscape then calls
the methods from ``Animal`` and gives it the necessary inputs for the animals to interact.



.. autoclass:: biosim.landscape.Landscape
   :members:
