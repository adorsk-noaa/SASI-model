from sasi.fishing.effort_model import EffortModel
from sasi.fishing.effort import Effort

class DAO_Effort_Model(EffortModel):

	def __init__(self, effort_dao=None, default_filters=None):
		self.effort_dao = effort_dao
		self.default_filters = default_filters

	def get_efforts(self, filters=None, override_default_filters=False):
		if self.default_filters and not filters:
			return self.effort_dao.get_efforts(filters=self.default_filters)
		elif self.default_filters and filters and not override_default_filters:
			combined_filters = self.default_filters + filters
			return self.effort_dao.get_efforts(filters=combined_filters)
		else:
			return self.effort_dao.get_efforts(filters=filters)

	def get_efforts_for_c_t(self, cell=None, time=None):
		filters = [
				{'attr': 'Cell.id', 'op': '==', 'value': cell.id},
				{'attr': 'time', 'op': '==', 'value': time}
				]
		if self.default_filters: filters.extend(self.default_filters)
		
		return self.effort_dao.get_efforts(filters=filters)

