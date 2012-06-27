class Cell(object):
    def __init__(self, id=None, type=None, type_id=None, geom=None, area=None, habitat_composition=None):
        self.id = id
        self.type = type
        self.type_id = type_id
        self.geom = geom
        self.area = area
        self.habitat_composition = habitat_composition
