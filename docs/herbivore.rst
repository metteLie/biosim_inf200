.. _herbivore:

Herbivore
==================================

``Herbivore`` is a subclass of ``Animal``. It feeds only on fodder and is marked as a prey. This
means that they can be eaten by carnivores (and humans if extra package is included).

The herbivores eat in priority defined by their fitness. The fittest herbivores eat first, which
leaves the weakest with less chance of surviving.
See :ref:`animals` and :ref:`parameters` for more information on how they behave.

.. autoclass:: biosim.herbivore.Herbivore
   :members: