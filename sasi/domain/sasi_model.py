import sasi.conf as conf
from sasi.domain import Result
import sys

class SASI_Model(object):

    def __init__(self, t0=0, tf=10, dt=1, cell_source=None, feature_source=None, effort_model=None, va=None, taus=None, omegas=None):

        # Start time.
        self.t0 = t0

        # End time.
        self.tf = tf

        # Timestep.
        self.dt = dt

        # Cells.
        self.cell_source = cell_source

        # Features.
        self.feature_source = feature_source

        # Get feature categories.
        # @TODO: get categories from config or VA.
        self.feature_categories = ['2']

        # Fishing effort model.
        self.effort_model = effort_model

        # Vulnerability Assessment
        self.va = va

        # tau (stochastic modifier for recovery)
        if not taus:
            taus = {
                    '0' : 1,
                    '1' : 2,
                    '2' : 5,
                    '3' : 10
                    }
            self.taus = taus

        # omega (stochastic modifier for damage)
        if not omegas:
            omegas = {
                    '0' : .10,
                    '1' : .25,
                    '2' : .50,
                    '3' : 1
                    }
            self.omegas = omegas

        # Results, grouped by time and cell.
        self.results_t_c = {}
        # Results, as a list.
        self.results = []

        self.setup()

    def setup(self):
        """
        This method creates lookups which can speed up model runs.
        """

        # Get habitat types, grouped by gear categories that can be applied to those
        # habitat types. 
        if conf.conf['verbose']: print >> sys.stderr, "Getting habitats by gear categories..."
        self.ht_by_gcat = self.va.get_habitats_by_gear_categories()

        # Get feature codes, grouped by gear categories that can be applied to those
        # feature types.
        if conf.conf['verbose']: print >> sys.stderr, "Getting features by gear categories..."
        self.f_by_gcat = self.va.get_features_by_gear_categories()

        # Get features grouped by category, keyed by habitat types.
        if conf.conf['verbose']: print >> sys.stderr, "Getting features by gear categories..."
        self.f_by_ht = self.va.get_features_by_habitats()

        # Create feature lookup to improve perfomance.
        if conf.conf['verbose']: print >> sys.stderr, "Creating features lookup..."
        self.features = {}
        for f in self.feature_source.all():
            self.features[f.id] = f

        # Create cells-habitat_type-feature lookup to improve perfomance.
        # Assumes static habitats.
        if conf.conf['verbose']: print >> sys.stderr, "Creating cells-habitat_type-feature lookup..."
        self.c_ht_f = self.get_c_ht_f_lookup()

        # Create effort lookup by cell and time to improve performance.
        if conf.conf['verbose']: print >> sys.stderr, "Creating cells-time-effort lookup..."
        self.c_t_e = self.get_c_t_e_lookup()

        # Initialize results, grouped by time and cell.
        if conf.conf['verbose']: print >> sys.stderr, "Initializing results..."
        for t in range(self.t0, self.tf + self.dt, self.dt):
            self.results_t_c[t] = {}
            for c in self.c_ht_f.keys():
                self.results_t_c[t][c] = {}

    def get_c_ht_f_lookup(self):

        # Initialize cell-habitat_type-feature lookup.
        c_ht_f = {}

        # For each cell...
        for c in self.cell_source.all():

            # Create entry in c_ht_f for cell.
            c_ht_f[c] = {
                    'ht': {}
                    }

            # For each habitat type in the cell's habitat composition...
            for ht, pct_area in c.habitat_composition.items():

                ht_key = ','.join(ht)

                # Create entry for ht in c_ht_f.
                c_ht_f[c]['ht'][ht_key] = {}

                # Save percent area.
                c_ht_f[c]['ht'][ht_key]['percent_cell_area'] = pct_area

                # Calculate habitat type area.
                c_ht_f[c]['ht'][ht_key]['area'] = c.area * pct_area

                # Get features for habitat, grouped by featured category.
                c_ht_f[c]['ht'][ht_key]['f'] = {}
                for feature_category, feature_ids in self.f_by_ht[ht_key].items():
                    features = [self.features[f_id] for f_id in feature_ids]
                    c_ht_f[c]['ht'][ht_key]['f'][feature_category] = features 

        return c_ht_f

    def get_c_t_e_lookup(self):

        # Initialize lookup.
        c_t_e = {}

        # For each effort in the model's time range...
        effort_counter = 0
        for e in self.effort_model.get_efforts(filters=[
            {'field': 'time', 'op': '>=', 'value': self.t0},
            {'field': 'time', 'op': '<=', 'value': self.tf},
            ]):

            effort_counter += 1
            if conf.conf['verbose']: 
                if (effort_counter % 1000) == 0: print >> sys.stderr, "effort: %s" % effort_counter


            # Create cell-time key.
            c_t_key = (e.cell, e.time)

            # Initialize lookup entries for cell-time key, if not existing.
            c_t_e.setdefault(c_t_key, [])

            # Add effort to lookup.	
            c_t_e[c_t_key].append(e)

        return c_t_e


    def run(self):

        # Iterate from t0 to tf...
        for t in range(self.t0, self.tf + 1, self.dt):
            self.iterate(t)

    def iterate(self, t):

        # For each cell...
        cell_counter = 0
        for c in self.c_ht_f.keys():

            if conf.conf['verbose']:
                if (cell_counter % 100) == 0: print >> sys.stderr, "\tc: %s" % cell_counter

            cell_counter += 1

            # Get contact-adjusted fishing efforts for the cell.
            cell_efforts = self.c_t_e.get((c,t),[])

            # For each effort...
            for effort in cell_efforts:

                # Get cell's habitat types which are relevant to the effort.
                relevant_habitat_types = []
                for ht in self.c_ht_f[c]['ht'].keys():
                    if ht in self.ht_by_gcat[effort.gear.category]: relevant_habitat_types.append(ht)

                # If there were relevant habitat types...
                if relevant_habitat_types:

                    # Calculate the total area of the relevant habitats.
                    relevant_habitats_area = sum([self.c_ht_f[c]['ht'][ht]['area'] for ht in relevant_habitat_types])

                    # For each habitat type...
                    for ht in relevant_habitat_types:

                        # Distribute the effort's swept area proportionally to the habitat type's area as a fraction of the total relevant area.
                        swept_area_per_habitat_type = effort.swept_area * (self.c_ht_f[c]['ht'][ht]['area']/relevant_habitats_area)

                        # Distribute swept area equally across feature categories.
                        # @TODO: maybe weight this? rather than just num categories?
                        swept_area_per_feature_category = swept_area_per_habitat_type/len(self.feature_categories)

                        # For each feature category...
                        for fc in self.feature_categories:

                            # Get the features for which the gear can be applied. 
                            relevant_features = []
                            for f in self.c_ht_f[c]['ht'][ht]['f'].get(fc,[]):
                                if f.id in self.f_by_gcat[effort.gear.category]: relevant_features.append(f)

                            # If there were relevant features...
                            if relevant_features:

                                # Distribute the category's effort equally over the features.
                                swept_area_per_feature = swept_area_per_feature_category/len(relevant_features)

                                # For each feature...
                                for f in relevant_features:

                                    # Get vulnerability assessment for the effort.
                                    vulnerability_assessment = self.va.get_assessment(
                                            gear_category = effort.gear.category,
                                            habitat_key = ht,
                                            feature_code = f.id,
                                            )

                                    # Get stochastic modifiers 
                                    omega = self.omegas.get(vulnerability_assessment['S'])
                                    tau = self.taus.get(vulnerability_assessment['R'])

                                    # Get or create the result corresponding to the
                                    # current set of parameters.
                                    result_key = (ht, effort.gear, f)
                                    (substrate_id,energy_id) = ht.split(',')
                                    result = self.get_or_create_result(t, c, result_key)

                                    # Add the resulting contact-adjusted
                                    # swept area to the a field.
                                    result.a += swept_area_per_feature

                                    # Calculate adverse effect swept area and add to y field.
                                    adverse_effect_swept_area = swept_area_per_feature * omega
                                    result.y += adverse_effect_swept_area

                                    # Calculate recovery per timestep.
                                    recovery_per_dt = adverse_effect_swept_area/tau

                                    # Add recovery to x field for future entries.
                                    for future_t in range(t + 1, t + tau + 1, self.dt):
                                        if future_t <= self.tf:
                                            future_result = self.get_or_create_result(future_t, c, result_key)
                                            future_result.x += recovery_per_dt

                                    # Calculate Z.
                                    result.z = result.x - result.y

                                    # Update znet
                                    result.znet += result.z

                                    # End of the iteration.

    def get_or_create_result(self, t, cell, result_key):
        (substrate_id,energy_id) = result_key[0].split(',')
        gear = result_key[1]
        feature = result_key[2]
        # If result for key does not exist yet, create it and
        # add it to the lookup and list.
        if not self.results_t_c[t][cell].has_key(result_key):
            new_result = Result(
                    t=t,
                    cell_id=cell.id,
                    gear_id=gear.id,
                    substrate_id=substrate_id,
                    energy_id=energy_id,
                    feature_id=feature.id,
                    a=0.0,
                    x=0.0,
                    y=0.0,
                    z=0.0,
                    znet=0.0
                    )
            self.results_t_c[t][cell][result_key] = new_result
            self.results.append(new_result)

        return self.results_t_c[t][cell][result_key]

