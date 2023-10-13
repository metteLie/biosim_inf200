.. _parameters:

Parameters
==================================

The formulas determining animal behaviour, and the properties of land types, use parameters.
These can be user specified, and even changed during simulations.
If none are provided, they all come with defaults, shown in the table below.

.. csv-table:: **Default Animal Parameters**
   :header: "Parameter", "Herbivore", "Carnivore", "Description"
   :widths: 15, 10, 10, 30

   ":math:`w_\text{birth}`, ``w_birth``", 8.0, "6", "Expected value of weight of newborn"
   ":math:`\sigma_\text{birth}`, ``sigma_birth``", 1.5, "1", "Standard deviation of weight of newborn"
   ":math:`\beta`, ``beta``", 0.9, "0.75", "Weight gained in kg from eating 1 kg of food (fodder or prey)"
   ":math:`\eta`, ``eta``", 0.05, "0.125", "Proportion of body weight lost each year"
   ":math:`a_\text{half}`, ``a_half``", 40, "40", "Halfway point (from 1 to 0) on age-fitness sigmoid"
   ":math:`\phi_\text{age}`, ``phi_age``", 0.6, "0.3", "Steepness of age-fitness sigmoid"
   ":math:`w_\text{half}`, ``w_half``", 10, "4", "Halfway point (from 0 to 1) on weight-fitness sigmoid"
   ":math:`\phi_\text{weight}`, ``phi_weight``", 0.1, "0.4", "Steepness of weight-fitness sigmoid"
   ":math:`\mu`, ``mu``", 0.25, "0.4", "Likelihood-coefficient for trying to migrate each year. Multiplied by fitness (:math:`\phi`)"
   ":math:`\gamma`, ``gamma``", 0.2, "0.8", "Likelihood-coefficient for giving birth, see :ref:`animals`"
   ":math:`\zeta`, ``zeta``", 3.5, "3.5", "To give birth, must be :math:`\zeta` times heavier :math:`w_\text{birth} + \sigma_\text{birth}`"
   ":math:`\xi`, ``xi``", 1.2, "1.1", "Weight lost giving birth is child's weight * :math:`\xi`"
   ":math:`\omega`, ``omega``", 0.4, "0.8", "Likelihood-coefficient of dying each year, multiplied by :math:`(1-\phi)`."
   ":math:`F`, ``F``", 10, "50", "Maximum weight of food one can eat per year"
   ":math:`\Delta\Phi_\text{max}`, ``DeltaPhiMax``", \-, "10", "Likelihood of killing a
   prey is equal to fitness difference divided by :math:`\Delta\Phi_\text{max}`"

.. csv-table:: **Default Landscape Parameters**
   :header: "Parameter", "Lowland", "Highland", "Desert", "Water"
   :widths: 15, 10, 10, 10, 10

   ":math:`f_\text{max}`, ``f_max``", 800, 200, 0, \-
   ":math:`habitable`", "``True``", "``True``", "``True``", "``False``"


.. automodule:: biosim.parameters
   :members:
   :undoc-members: default_animal_parameters, default_land_parameters
