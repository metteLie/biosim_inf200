
import pytest
from biosim.simulation import BioSim


class TestBioSim:

    @pytest.fixture(autouse=True)
    def create_sim(self):
        self.sim = BioSim(island_map="WWW\nWLW\nWWW", ini_pop=[], seed=1, vis_years=0)

    def test_set_unknown_species(self):
        with pytest.raises(ValueError):
            self.sim.set_animal_parameters('Hippo', {'F': 123})

    def test_set_unknown_landscape(self):
        with pytest.raises(ValueError):
            self.sim.set_landscape_parameters('X', {'f_max': 123})

    def test_set_unknown_params(self):
        with pytest.raises(ValueError):
            self.sim.set_animal_parameters('Herbivore', {'stigma': 123})
        with pytest.raises(ValueError):
            self.sim.set_landscape_parameters('L', {'stigma': 123})

    def test_set_invalid_param_value(self):
        with pytest.raises(ValueError):
            self.sim.set_animal_parameters('Herbivore', {'F': -20})
        with pytest.raises(ValueError):
            self.sim.set_animal_parameters('Herbivore', {'eta': 2})
        with pytest.raises(ValueError):
            self.sim.set_landscape_parameters('L', {'f_max': -3})
