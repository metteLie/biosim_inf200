import matplotlib.pyplot as plt
import numpy as np
from .graphics import Graphics


class BioGraphics(Graphics):
    def __init__(self, island_map, vis_years, ymax_animals, cmax_animals, hist_specs,
                 img_dir=None, img_base=None, img_fmt=None, img_years=None):
        """
        :param ymax_animals: Number specifying y-axis limit for graph showing animal numbers
        :param cmax_animals: Dict specifying color-code limits for animal densities
        :param hist_specs: Specifications for histograms, see below
        :param vis_years: years between visualization updates (if 0, disable graphics)
        :param img_dir: String with path to directory for figures (default None: no image saving)
        :param img_base: String with beginning of file name for figures
        :param img_fmt: String with file type for figures, e.g. 'png'
        :param img_years: years between visualizations saved to files (default: vis_years) \
        Must be a multiple of vis_years

        If ymax_animals is None, the y-axis limit should be adjusted automatically.
        If cmax_animals is None, sensible, fixed default values should be used.
        cmax_animals is a dict mapping species names to numbers, e.g.,

           {'Herbivore': 50, 'Carnivore': 20}

        hist_specs is a dictionary with one entry per property for which a histogram shall be shown.
        For each property, a dictionary providing the maximum value and the bin width must be
        given, e.g.,

            {'weight': {'max': 80, 'delta': 2}, 'fitness': {'max': 1.0, 'delta': 0.05}}

        Permitted properties are 'weight', 'age', 'fitness'.

        If img_dir is None, no figures are written to file. Filenames are formed as

            f'{os.path.join(img_dir, img_base}_{img_number:05d}.{img_fmt}'

        where img_number are consecutive image numbers starting from 0.

        img_dir and img_base must either be both None or both strings.
        """
        if img_years is None:
            img_years = vis_years
        elif vis_years != 0 and img_years % vis_years != 0:
            raise ValueError("img_years must be a multiple of vis_years")
        super().__init__(img_dir, img_base, img_fmt, img_years)
        self.vis_years = vis_years
        self.ymax_animals = ymax_animals
        self.cmax_animals = cmax_animals if cmax_animals is not None else {}
        self.hist_specs = hist_specs if hist_specs is not None else {}
        self.img_years = img_years if img_years is not None else self.vis_years
        self.island_map = island_map
        self.num_years = 0

        self.fig = None

        self.island_ax = None
        self.species_pop_ax = None
        self.heatmap_ax = {}
        self.fitness_histogram_ax = None
        self.age_histogram_ax = None
        self.weight_histogram_ax = None

        self.year_text = None
        self.species_population_axis = {}
        self.heatmap_axis = {}

    def setup(self, num_years):
        """
        :param num_years: The number of years we expect to visualize

        Prepares the visualization graphs for ``num_years`` of future simulation.
        This scales the x-axis of historical plots.

        Can be called again, if the total number of years we want to simulate has changed.
        """
        self.num_years = num_years

        if self.fig is None:
            self.fig = (fig := plt.figure())

            # normal subplots
            self.island_ax = fig.add_subplot(3, 3, 1)
            self.species_pop_ax = fig.add_subplot(3, 3, 3)
            self.heatmap_ax['Herbivore'] = fig.add_subplot(3, 3, 4)
            self.heatmap_ax['Human'] = fig.add_subplot(3, 3, 5)
            self.heatmap_ax['Carnivore'] = fig.add_subplot(3, 3, 6)
            for heatmap_ax in self.heatmap_ax.values():
                heatmap_ax.axis('off')
            self.fitness_histogram_ax = fig.add_subplot(3, 3, 7)
            self.age_histogram_ax = fig.add_subplot(3, 3, 8)
            self.weight_histogram_ax = fig.add_subplot(3, 3, 9)

            self.island_ax.set_title('Island', fontsize=7)
            self.species_pop_ax.set_title('Animal count', fontsize=7)

            self._plot_map()
            self.fig.tight_layout(pad=1.1, w_pad=0., h_pad=1.9)

            # axes for text
            axt = fig.add_axes([0.4, 0.8, 0.2, 0.2])  # llx, lly, w, h
            axt.axis('off')  # turn off coordinate system

            self.year_text = axt.text(0.5, 0.5, '',
                                      horizontalalignment='center',
                                      verticalalignment='center',
                                      transform=axt.transAxes)  # relative coordinates

        self.species_pop_ax.set_xlim(0, num_years)
        self.species_pop_ax.set_ylim(0, self.ymax_animals)

    def _plot_map(self):
        #                   R    G    B
        rgb_value = {'W': (0.0, 0.0, 1.0),  # blue
                     'L': (0.0, 0.6, 0.0),  # dark green
                     'H': (0.5, 1.0, 0.5),  # light green
                     'D': (1.0, 1.0, 0.5)}  # light yellow

        map_rgb = [[rgb_value[column] for column in row]
                   for row in self.island_map.splitlines()]

        ax_im = self.island_ax
        ax_im.imshow(map_rgb)
        ax_im.set_xticks(range(0, len(map_rgb[0]), 4))
        ax_im.set_xticklabels(range(1, 1 + len(map_rgb[0]), 4))
        ax_im.set_yticks(range(0, len(map_rgb), 4))
        ax_im.set_yticklabels(range(1, 1 + len(map_rgb), 4))

        ax_lg = self.island_ax.inset_axes([1.1, 0.1, 0.1, 0.8])  # llx, lly, w, h
        ax_lg.axis('off')
        for ix, name in enumerate(('Water', 'Lowland',
                                   'Highland', 'Desert')):
            ax_lg.add_patch(plt.Rectangle((0., ix * 0.2), 0.3, 0.1,
                                          edgecolor='none',
                                          facecolor=rgb_value[name[0]]))
            ax_lg.text(0.35, ix * 0.2, name, transform=ax_lg.transAxes)

    def update(self, biosim):
        """
        :param biosim: the biosim with the state we want to visualize

        Uses the properties on the BioSim instance to fill heatmaps,
        histograms and plots with data.

        If the current year is a multiple of ``vis_years``,
        the plots are displayed on the screen. If ``vis_years`` is 0,
        nothing ever gets plotted.

        Will possibly also save an image file of the finished graphs,
        if year is a multiple of img_years and images are enabled.
        """
        if self.vis_years == 0:
            return

        self._plot_species_count(biosim.year, biosim.num_animals_per_species)
        species_cell_counts = biosim.num_animals_per_cell_per_species
        for species in species_cell_counts:
            self._plot_population_map(species, species_cell_counts)
        self._plot_hist_fitness(biosim.fitness_per_species)
        self._plot_hist_age(biosim.ages_per_species)
        self._plot_hist_weight(biosim.weights_per_species)

        self.year_text.set_text(f"Year: {biosim.year}")
        self.fig.canvas.flush_events()

        if biosim.year % self.vis_years == 0:
            plt.pause(1e-6)

        self._save_graphics(biosim.year)

    def _plot_species_count(self, year, dict_species_count):
        for specie, count in dict_species_count.items():
            if specie not in self.species_population_axis:
                self.species_population_axis[specie] = self.species_pop_ax.plot([], [], '-')[0]
            xdata, ydata = self.species_population_axis[specie].get_data()
            self.species_population_axis[specie].set_data(np.append(xdata, year),
                                                          np.append(ydata, count))

            if self.ymax_animals is None:
                _, ymax = self.species_pop_ax.get_ylim()
                self.species_pop_ax.set_ylim(0, max(ymax, count))

    def _plot_population_map(self, species, species_cell_counts):
        if species not in self.heatmap_ax:
            return

        pop_map = [[species_cell_counts[species][(i_row + 1, i_col + 1)]
                    for i_col, col in enumerate(row)]
                   for i_row, row in enumerate(self.island_map.splitlines())]
        pop_cmax = self.cmax_animals.get(species, max(1, max(max(line) for line in pop_map)))
        if species in self.heatmap_axis:
            self.heatmap_axis[species].set_data(pop_map)
            _, current_cmax = self.heatmap_axis[species].get_clim()
            self.heatmap_axis[species].set_clim((0, max(current_cmax, pop_cmax)))
        else:
            self.heatmap_ax[species].set_title(f'{species} heatmap', fontsize=7)
            self.heatmap_ax[species].axis('on')
            self.heatmap_axis[species] = self.heatmap_ax[species].imshow(
                pop_map, interpolation='nearest',
                vmin=0, vmax=pop_cmax)
            plt.colorbar(self.heatmap_axis[species], ax=self.heatmap_ax[species],
                         orientation='vertical')

    def _plot_hist_fitness(self, dict_species_fitness):
        bins = None
        if 'fitness' in self.hist_specs:
            max_fitness = self.hist_specs['fitness']['max']
            delta = self.hist_specs['fitness']['delta']
            bins = np.linspace(0, max_fitness, int(max_fitness / delta) + 1)

        self.fitness_histogram_ax.clear()
        self.fitness_histogram_ax.set_title('Fitness', fontsize=7)
        self.fitness_histogram_ax.hist(dict_species_fitness.values(), bins=bins, histtype='step')

    def _plot_hist_age(self, dict_species_age):
        bins = None
        if 'age' in self.hist_specs:
            max_age = self.hist_specs['age']['max']
            delta = self.hist_specs['age']['delta']
            bins = np.linspace(0, max_age, int(max_age / delta) + 1)

        self.age_histogram_ax.clear()
        self.age_histogram_ax.set_title('Age', fontsize=7)
        self.age_histogram_ax.hist(dict_species_age.values(), label=list(dict_species_age.keys()),
                                   bins=bins, histtype='step')
        self.age_histogram_ax.legend(bbox_to_anchor=(0.5, 3.), loc='lower center',
                                     borderaxespad=0.)

    def _plot_hist_weight(self, dict_species_weight):
        bins = None
        if 'weight' in self.hist_specs:
            max_weight = self.hist_specs['weight']['max']
            delta = self.hist_specs['weight']['delta']
            bins = np.linspace(0, max_weight, int(max_weight / delta) + 1)

        self.weight_histogram_ax.clear()
        self.weight_histogram_ax.set_title('Weight', fontsize=7)
        self.weight_histogram_ax.hist(dict_species_weight.values(), bins=bins, histtype='step')
