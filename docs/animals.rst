.. _animals:

Animals
==================================

All creatures in BioSim are subclasses of ``Animal``. The ``Animal`` class contains methods that
are equal to all, but the outcome will depend on the parameters set for each species.
See ``Parameters``.

New animals can easily be added, by creating a new subclass of ``Animal``.
Each subclass can override the ``Animal`` methods if desired. For an example of adding new animals
see :ref:`humans`.

.. autoclass:: biosim.animals.Animal
   :members: