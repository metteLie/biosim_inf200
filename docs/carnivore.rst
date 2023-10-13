.. _carnivore:

Carnivore
==================================

Carnivore is a subclass of ``Animal``. It feeds only on prey and is not marked as a prey itself.
This means that they only attack herbivores and cannot be eaten by other carnivores (or humans
if extra package is included).

The carnivores eat in random order, but after all herbivores (and before humans). They attack the
weakest prey first, but it is not guaranteed that they will be able to kill it. They will
try the next prey as long as there are unattempted kills left and they're still hungry.

See :ref:`animals` and :ref:`parameters` for more information on how they behave.

.. autoclass:: biosim.carnivore.Carnivore
   :members:
