class Habitat_Type(object):

	def __init__(self, id=None, substrate=None, energy=None, features=None):
		self.substrate = substrate
		self.energy = energy
		self.features = features
		self.id = "%s,%s" % (self.substrate.id,self.energy)

