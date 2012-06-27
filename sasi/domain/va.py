class VulnerabilityAssessment(object):

	def __init__(self, rows=[]):

		self.assessments = self.make_assessments_from_rows(rows)
	
	def make_assessments_from_rows(self, rows):
		# Save rows, keyed by (GEAR_CATEGORY, SUBSTRATE_CODE, FEATURE_CODE,ENERGY)
		assessments = {}
		for r in rows:

			key = (r['GEAR_CATEGORY'], r['SUBSTRATE_CODE'], r['FEATURE_CODE'], r['ENERGY'])
			assessments[key] = r

		return assessments

	def get_assessment(self, habitat_key='', gear_category='', feature_code=''):
		(substrate_code,energy) = self.get_hab_key_parts(habitat_key=habitat_key)
		key = (gear_category, substrate_code, feature_code, energy)
		return self.assessments.get(key, None)

	def get_susceptibility(self, **kwopts):
		assessment = self.get_assessment(**kwopts)
		if assessment:
			return assessment['S']


	def get_recovery(self, **kwopts):
		assessment = self.get_assessment(**kwopts)
		if assessment:
			return assessment['R']

	def get_features_by_habitats(self):
		f_by_h = {}
		for key, assessment in self.assessments.items():
			hab_key = self.get_hab_key(assessment=assessment)
			features_for_hab = f_by_h.setdefault(hab_key,{})
			features_for_category = features_for_hab.setdefault(assessment['FEATURE_CLASS_CODE'],set())
			features_for_category.add(assessment['FEATURE_CODE'])
		return f_by_h

	def get_features(self):
		features = {} 
		for key, assessment in self.assessments.items():
			features[assessment['FEATURE_CODE']] = {
					'FEATURE_CODE': assessment['FEATURE_CODE'],
					'FEATURE_CLASS_CODE': assessment['FEATURE_CLASS_CODE'],
					'FEATURE': assessment['FEATURE']
					}
		return features
	
	def get_substrates(self):
		substrates = {} 
		for key, assessment in self.assessments.items():
			substrates[assessment['SUBSTRATE_CODE']] = {
					'SUBSTRATE_CODE': assessment['SUBSTRATE_CODE'],
					'SUBSTRATE': assessment['SUBSTRATE']
					}
		return substrates

	def get_hab_key(self, assessment=None):
		return ','.join([assessment['SUBSTRATE_CODE'], assessment['ENERGY']])

	def get_hab_key_parts(self, habitat_key=None):
		return habitat_key.split(',')

	def get_gear_categories_by_habitats(self):
		gear_category_by_h = {}
		for key, assessment in self.assessments.items():
			hab_key = self.get_hab_key(assessment=assessment)
			gear_categorys_for_hab = gear_category_by_h.setdefault(hab_key,set())
			gear_categorys_for_hab.add(assessment['GEAR_CATEGORY'])
		return gear_category_by_h
	
	def get_habitats_by_gear_categories(self):
		h_by_gear_category = {}
		for key, assessment in self.assessments.items():
			hab_key = self.get_hab_key(assessment=assessment)
			habs_for_gear_category = h_by_gear_category.setdefault(assessment['GEAR_CATEGORY'], set())
			habs_for_gear_category.add(hab_key)
		return h_by_gear_category

	def get_features_by_gear_categories(self):
		f_by_g = {}
		for key, assessment in self.assessments.items():
			features_for_gears = f_by_g.setdefault(assessment['GEAR_CATEGORY'], set())
			features_for_gears.add(assessment['FEATURE_CODE'])
		return f_by_g

	def get_habitats_for_gear_category(self, gear_category):
		habitats = set()
		for key, assessment in self.assessments.items():
			if assessment['GEAR_CATEGORY'] == gear_category:
				hab_key = self.get_hab_key(assessment=assessment)
				habitats.add(hab_key)
		return habitats

	def get_features_for_gear_category(self, gear_category):
		features = set()
		for key, assessment in self.assessments.items():
			if assessment['GEAR_CATEGORY'] == gear_category:
				features.add(assessment['FEATURE_CODE'])
		return features

	def get_gear_categories(self):
		gear_categories = {} 
		for key, assessment in self.assessments.items():
			gear_categories[assessment['GEAR_CATEGORY']] = {
					'GEAR_CATEGORY': assessment['GEAR_CATEGORY'],
					}
		return gear_categories

	def get_habitats(self):
		habitats = set()
		for key, assessment in self.assessments.items():
			hab_key = self.get_hab_key(assessment=assessment)
			habitats.add(hab_key)
		return habitats

